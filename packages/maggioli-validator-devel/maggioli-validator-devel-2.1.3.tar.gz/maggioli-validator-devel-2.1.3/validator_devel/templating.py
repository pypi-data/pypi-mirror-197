import time

import pkg_resources
import requests
from dynaconf import settings
from .filesystem import get_all_dependencies, find_modules_by_path
from aiohttp import streamer

import jinja2
import tempfile
import logging
import shutil
import os
import zipfile
import uuid
import click

__environment = None
__temporary_dir = None
__holding = {}

def get_modules_path():
    return settings.get('modules_path')

def get_validator_path():
    path= settings.get('validator_path')
    print(f'validator path: {path}')
    return path

def get_stu3_validator_path():
    return settings.get('stu3_validator_path')

def init():
    """"Start the Jinja2 engine and loader."""
    global __environment, __temporary_dir

    if get_modules_path():
        __environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(get_modules_path()),
            extensions=['jinja2.ext.do'],
        )

    if __temporary_dir is None:
        __temporary_dir = os.path.join(click.get_app_dir("validator-devel"), 'download')

def shutdown():
    """Teardown function, delete all temporary modules."""
    logging.debug("delete templating.")


def get_module_loader():
    if __environment is None:
        init()

    return __environment

def get_module_html(module: dict):
    """Return a renderized module."""
    module_path = module['file_path']
    if module_path.startswith(get_modules_path()):
        module_path = module_path[len(get_modules_path()):]

    if os.sep != '/':
        module_path = module_path.replace(os.sep, '/')

    logging.debug(f"try to render: {module_path}")
    loader = get_module_loader()
    try:
        template = loader.get_template(module_path)
    except jinja2.TemplateNotFound:
        return None

    result = template.render()
    return result

def zipdir(path, ziph, exclude: list=[]):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        os.chdir(root)
        for file in files:
            if file in exclude:
                continue

            ziph.write(file)

def get_module_dependencies(module: dict, nested=False):
    modules = []

    extends = module.get('extends', 'base.html')
    if extends != 'base.html':
        extend_module = find_modules_by_path(extends)

        if not extend_module:
            logging.error(f'can\'t find this extend {extends}')
            raise jinja2.exceptions.TemplateNotFound(extends)

        logging.debug(f'nested search for {extend_module["urn"]}')
        modules.extend(get_module_dependencies(extend_module, True))


    if module.get('urn', None):
        logging.debug(f'find dependencies for {module["urn"]}')
        modules.extend(get_all_dependencies(module['urn']))
    elif not nested:
        modules.append(module)

    return modules


def prepare_modules(modules: list):
    """Preapare a list of modules in a zip files, the files are not streamed
    because before is checked if there are error, and uuid is retrived that is
    a valid code for request the prepared packet."""
    temp_dir = tempfile.TemporaryDirectory()
    dir_name = temp_dir.name

    for m in modules:
        logging.debug(f"create module {m['filename']} in {dir_name}")
        prefix = '_'.join(m['folders'])
        path = os.path.join(dir_name, f'{prefix} {m["filename"]}')
        with open(path, 'w', encoding="utf8") as f_m:
            module_body = get_module_html(m)
            f_m.write(module_body)

    unique_code = str(uuid.uuid4())

    zip_path = os.path.join(__temporary_dir, f"{unique_code}.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(dir_name, zipf)

    global __holding
    __holding[unique_code] = zip_path

    try:
        temp_dir.cleanup()
    except PermissionError:
        # Ignore permission error under windows.
        pass
    finally:
        return unique_code


def prepare_single_module(module, key):
    module_body = get_module_html(module)
    prefix = '_'.join(module['folders'])
    html_path = os.path.join(__temporary_dir, f"{key}.html")
    global __holding
    __holding[f"{key}_single"] = html_path
    with open(html_path, "w", encoding="utf8") as f:
        f.write(module_body)


class PDFException(Exception):
    pass

def generate_pdf(module, key):
    module_body = get_module_html(module)
    stu3_url = settings.get("pdf_stu3_url")
    result = requests.post(f"{stu3_url}/modulo_html/raw_pdf_generate/{key}", data=module_body.encode('utf-8'))
    if result.status_code != 200:
        raise PDFException(f"Error {result.status_code} in pdf generation: {result.text}")
    result = None
    start_time = time.time()
    while time.time() - start_time < settings.get("pdf_timeout"):
        result = requests.get(f"{stu3_url}/modulo_html/raw_pdf_download/{key}")
        if result.status_code == 200:
            break
        time.sleep(1)
    if not result or result.status_code != 200:
        raise PDFException(f"Timeout in pdf generation: {result.text}")

    pdf_path = os.path.join(__temporary_dir, f"{key}.pdf")
    global __holding
    __holding[f"{key}_pdf"] = pdf_path
    with open(pdf_path, "wb") as f:
        f.write(result.content)

@streamer
async def download_file(writer, code: str):
    """Stream out a prepared file."""
    path = __holding.get(code, None)
    if path is None:
        logging.error(f"A file with {code} is requested, but there isn't")
        return None

    with open(path, 'rb') as f:
        chunk = f.read(2 ** 16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2 ** 16)

    os.remove(path)
