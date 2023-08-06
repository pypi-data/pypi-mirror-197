import pkg_resources
import logging

from dynaconf import settings
from .views import (
    index, module, module_websocket_handler, module_html, module_prepare_download,
    folder_prepare_download, download, edit_module, build_generic_rest, build_generic_proxy, module_prepare_pdf,
    download_pdf, module_prepare_download_single, download_single, stu2_validation_settings,
    stu2_municipalty_info
)
from .templating import get_validator_path, get_stu3_validator_path


def get_static_path():
    return pkg_resources.resource_filename("validator_devel", "static")

def generate_urls_from_settings(app):
    urls = settings.get('urls')
    if urls:
        for (url, data) in urls.items():
            if isinstance(data, str) and data.startswith('http'):
                app.router.add_route('*', url, build_generic_proxy(data))
                continue

            headers = {
                'Content-Type': 'application/json'
            }
            if 'headers' in data:
                headers.update(data['headers'])

            app.router.add_get(url, build_generic_rest(data['body'], headers))


def setup_routes(app):

    # Validator handler.
    app.router.add_static('/module/validator/', path=get_validator_path(), name='validator')
    app.router.add_static('/module/stu3/validator/', path=get_stu3_validator_path(), name='stu3_validator')
    app.router.add_static('/module/appoggio/', path=pkg_resources.resource_filename('validator_devel', 'appoggio'), name='stu3_appoggio')

    app.router.add_get('/ws', module_websocket_handler)
    app.router.add_get('/module/{module_key}/download', module_prepare_download)
    app.router.add_get('/module/{module_key}/download_single', module_prepare_download_single)
    app.router.add_get('/module/{module_key}/pdf', module_prepare_pdf)
    app.router.add_get('/module/{module_key}/edit', edit_module)
    app.router.add_get('/module/{module_key}', module_html)
    app.router.add_get('/module', module)

    app.router.add_get('/folder/{folder}/download', folder_prepare_download)
    app.router.add_get('/download/{uuid}', download)
    app.router.add_get('/download-pdf/{key}', download_pdf)
    app.router.add_get('/download-single/{key}', download_single)
    app.router.add_get('/validazione_dati/get_impostazioni_validazioni', stu2_validation_settings)
    app.router.add_get('/sportello_telematico/dati_comune/', stu2_municipalty_info)

    # STU3 Rest mockup.
    generate_urls_from_settings(app)

    # Frontend handler.
    app.router.add_static('/', path=get_static_path(), name='static', show_index=True)
