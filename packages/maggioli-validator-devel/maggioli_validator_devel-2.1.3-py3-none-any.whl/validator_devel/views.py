import logging
import os
import tempfile
import time

import click
import jinja2
import traceback
import sys

from urllib.parse import urlparse

import pkg_resources
from dynaconf import settings
from aiohttp import web, WSMsgType, http_exceptions, ClientSession
from .filesystem import get_modules, find_module, get_all_modules_in_folder
from .templating import (
    get_module_html, get_validator_path, get_module_dependencies,
    download_file, prepare_modules, generate_pdf, prepare_single_module, PDFException
)


async def index(request):
    """Retrieve the index of site."""
    return web.Response(text="validator devel")


async def module(request):
    """Return all modules as JSON."""
    data = get_modules()
    return web.json_response(data)


async def module_prepare_download(request):
    """Prepare download for a module, if all is ok return a uuid else
    return an error."""
    key = request.match_info['module_key']
    module = find_module(key)
    if module is None:
        raise web.HTTPNotFound()

    try:
        modules = get_module_dependencies(module)
        uuid = prepare_modules(modules)

        data = {
            "uuid": uuid,
        }
    except KeyError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = traceback.format_exception(exc_type, exc_value, exc_traceback)
        data = {
            "error": {
                "stacktrace": error,
                "type": "module_request.key_error",
                "request": key,
                "missing_key": e.args[0],
            }
        }
    except (jinja2.TemplateError, jinja2.TemplateRuntimeError, jinja2.TemplateSyntaxError) as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = traceback.format_exception(exc_type, exc_value, exc_traceback)
        data = {
            "error": {
                "stacktrace": error,
                "type": "module_request.template_not_found",
                "request": key,
                "missing_templates": e.templates,
            }
        }

    return web.json_response(data)


async def module_prepare_download_single(request):
    """Prepare download for a single module, if all is ok download it else
    return an error."""
    key = request.match_info['module_key']
    m = find_module(key)
    if m is None:
        raise web.HTTPNotFound()
    try:
        prepare_single_module(m, key)
    except KeyError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return web.json_response({
            "error": {
                "stacktrace": error,
                "type": "module_request.key_error",
                "request": key,
                "missing_key": e.args[0],
            }
        })
    except (jinja2.TemplateError, jinja2.TemplateRuntimeError, jinja2.TemplateSyntaxError) as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return web.json_response({
            "error": {
                "stacktrace": error,
                "type": "module_request.template_not_found",
                "request": key,
                "missing_templates": e.templates,
            }
        })

    return web.json_response({
        "uuid": key,
    })


async def module_prepare_pdf(request):
    download_dir = os.path.join(click.get_app_dir("validator-devel"), 'download')
    """Prepare pdf for a module, if all is ok return a uuid else
    return an error."""
    key = request.match_info['module_key']
    module = find_module(key)
    if module is None:
        raise web.HTTPNotFound()

    try:
        generate_pdf(module, key)
    except PDFException as e:
        return web.json_response({
            "error": {
                "stacktrace": e.args[0].splitlines(),
                "type": "generate_pdf.error",
                "request": key,
            }
        })
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return web.json_response({
            "error": {
                "stacktrace": error,
                "type": "generate_pdf.error",
                "request": key,
            }
        })

    return web.json_response({
        "uuid": key,
    })

async def folder_prepare_download(request):
    """Return a zip that contains all modules and his dependencies."""
    key = request.match_info['folder']
    with_deps = request.query.get('with_deps', False)
    key = '/'.join(key.split('-'))
    modules = get_all_modules_in_folder(key)
    if not modules :
        raise web.HTTPNotFound()

    try:
        if with_deps:
            all_deps = []
            for module in modules:
                all_deps = all_deps + get_module_dependencies(module)
            all_deps = list({v['key']: v for v in all_deps}.values())
        else:
            all_deps = list(modules)

        uuid = prepare_modules(all_deps)

        data = {
            "uuid": uuid,
        }

    except KeyError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = traceback.format_exception(exc_type, exc_value, exc_traceback)
        data = {
            "error": {
                "stacktrace": error,
                "type": "folder_request.key_error",
                "request": key,
                "missing_key": e.args[0],
            }
        }
    except (jinja2.TemplateError, jinja2.TemplateRuntimeError, jinja2.TemplateSyntaxError) as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = traceback.format_exception(exc_type, exc_value, exc_traceback)
        data = {
            "error": {
                "stacktrace": error,
                "type": "folder_request.template_not_found",
                "request": key,
                "missing_templates": e.templates,
            }
        }

    return web.json_response(data)

async def download(request):
    uuid = request.match_info['uuid']

    return web.Response(
        body=download_file(uuid),
        headers={"Content-disposition": "attachment; filename=modules.zip"}
    )

async def download_pdf(request):
    key = request.match_info['key']
    module = find_module(key)
    prefix = '_'.join(module['folders'])
    pdf_filename = f"{prefix}{module['filename'].rsplit('.', 1)[0]}.pdf"
    return web.Response(
        body=download_file(f"{key}_pdf"),
        headers={"Content-disposition": f"attachment; filename={pdf_filename}", "Content-Type": "application/pdf"}
    )


async def download_single(request):
    key = request.match_info['key']
    module = find_module(key)
    prefix = '_'.join(module['folders'])
    html_filename = f"{prefix}{module['filename']}"
    return web.Response(
        body=download_file(f"{key}_single"),
        headers={"Content-disposition": f"attachment; filename={html_filename}", "Content-Type": "text/html"}
    )

from bs4 import BeautifulSoup
async def module_html(request):
    """Return the renderized HTML module."""
    key = request.match_info['module_key']
    module = find_module(key)
    if module is None:
        raise web.HTTPNotFound()

    try:
        body = get_module_html(module)
    except (jinja2.TemplateError, jinja2.TemplateRuntimeError, jinja2.TemplateSyntaxError):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        body = traceback.format_exception(exc_type, exc_value, exc_traceback)
        body = '\n'.join(body)
        logging.debug("Print a debug error for Exception.")

    if not body:
        raise web.HTTPNotFound()

    # Handle STU3 query field.
    if request.query.get('stu3'):
        soup = BeautifulSoup(body, 'html.parser')
        form = soup.find('form')
        stu3_base_path = pkg_resources.resource_filename('validator_devel', 'stu3_base.html.j2')
        with open(stu3_base_path, 'r') as f:
            stu3_base = f.read()

        stu3_template = jinja2.Template(stu3_base)

        return web.Response(body=stu3_template.render(module=form, urn=module["urn"]), headers={'content-type': 'text/html'})

    return web.Response(body=body, headers={'content-type': 'text/html'})


async def module_websocket_handler(request):
    """Handle websocket connection, is the update channel for module data."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    logging.debug("open a new websocket")
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
                logging.debug("close a websocket")
        elif msg.type == WSMsgType.ERROR:
            logging.error(f"closed a socket async with exception {ws.exception()}")

    return ws


async def edit_module(request):
    """Check the module and open the default editor."""
    key = request.match_info['module_key']
    module = find_module(key)
    if module is None:
        raise web.HTTPNotFound()
    else:
        import click
        click.launch(module['file_path'])

    return web.json_response({'status': 'ok'})


async def home(request):
    raise web.HTTPFound(location="/index.html")


def build_generic_rest(body, headers):
    async def view(request):
        return web.Response(
            body= body,
            headers= headers,
        )

    return view


def build_generic_proxy(endpoint):
    async def proxy(request):
        logging.debug(f"proxy on {request.path} to {endpoint}")
        async with ClientSession(auto_decompress=False) as session:
            body = await request.read()
            headers = dict(request.headers)
            o = urlparse(endpoint)
            if o.hostname is not None:
                headers['Host'] = o.hostname

            async with session.request(request.method, endpoint, data=body, headers=headers) as response:
                content = await response.content.read()

                return web.Response(
                    headers=response.headers,
                    status=response.status,
                    body=content
                )

    return proxy


def stu2_validation_settings(request):
    return web.json_response({
      "url_catview": "",
      "url_geostreets": "",
      "url_gfmaplet": "",
      "non_usa_catview": 0,
      "versione": "",
      "stilehtml": None,
      "catasto": {
        "mappa": "ctr",
        "service": "basemap_ortofoto",
        "idlayer": " "
      },
      "toponomastica": {
        "mappa": "ctr",
        "service": "basemap_ortofoto",
        "idlayer": " "
      },
      "abilitazione": {
        "Valida catasto": 0,
        "Valida toponomastica": 0,
        "Visualizza catasto in mappa": 0,
        "Visualizza toponomastica in mappa": 0,
        "Richiedi catasto": 0,
        "Richiedi toponomastica": 0
      }
    })


def stu2_municipalty_info(request):
    return web.json_response(["MAGGIOLI", None, "IT", "IT"])
