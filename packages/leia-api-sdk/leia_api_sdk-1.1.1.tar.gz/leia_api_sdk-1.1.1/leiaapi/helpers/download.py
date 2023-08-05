import io
import logging
from pathlib import Path
from typing import Optional, Union, Dict, List, Tuple, Set, Callable

from tqdm.auto import tqdm
from urllib3 import HTTPResponse

from leiaapi.generated.api import ApplicationAdminApi, ModelAdminApi
from leiaapi.generated.api_client import ApiClient
from leiaapi.generated.models import Application, Model
from leiaapi.generated.rest import ApiException

logger = logging.getLogger(__name__)


class FileIncompleteError(BaseException):
    pass


def download_model(token: str, model: Union[Model, Tuple[str, str], Tuple[str, str, Optional[int]]], save_folder: Optional[Union[Path, str]] = None, overwrite: bool = False, use_tqdm: bool = True, client: Optional[ApiClient] = None,
                   fn_filename: Callable[[Union[Model, Tuple[str, str], Tuple[str, str, Optional[int]]]], Union[str, Path]] = lambda model: f"{model.name}.model"):
    if isinstance(model, Model):
        model_id = model.id
        application_id = model.application_id
        total_size = int(model.size)
    elif isinstance(model, tuple):
        if len(model) == 2:
            model_id, application_id = model
            total_size = None
        else:
            model_id, application_id, total_size = model
    else:
        raise ValueError("model parameter not valid")

    file_name = fn_filename(model)
    api = ModelAdminApi(client)

    if save_folder is not None:
        if not isinstance(save_folder, Path):
            save_folder = Path(save_folder)
        if (save_folder / file_name).exists() and (total_size is None or total_size < 0 or total_size == (save_folder / file_name).stat().st_size) and not overwrite:
            logger.info(f'ignore {model_id}, same file already exist on disk')
            return save_folder / file_name

        if not save_folder.is_dir():
            save_folder.mkdir(parents=True, exist_ok=True)

        logger.info(f"Start downloading Model: {model_id} - Application: {application_id} - FileName: {save_folder / file_name} - size: {model_id} ({total_size / 1024 / 1024}Mo)")
    else:
        logger.info(f"Start downloading Model: {model_id} - Application: {application_id} - In memory: {file_name} - size: {model_id} ({total_size / 1024 / 1024}Mo)")
    resp: Optional[HTTPResponse] = None
    while resp is None or resp.status != 200:
        # logger.info(f'Calling {api.admin_get_model_contents.settings["endpoint_path"].format(**model._data_store, model_id=model.id)}')

        resp = api.admin_get_model_contents_with_http_info(token, model.application_id, model.id)

        if resp.status != 200:
            # if exit_on_error:
            # raise Exception(
            #     f'Cannot download {api.admin_get_model_contents.settings["endpoint_path"].format(**model._data_store, model_id=model.id)}, RETURN: {resp.status}')
            pass

    if not use_tqdm:
        logger.info(f"Downloading {model_id} with size {total_size}")

    try:
        if save_folder is None:
            f = io.BytesIO()
            read_stream(resp, f, use_tqdm)
            res = f.getvalue()
        else:
            with (save_folder / file_name).open("wb") as f:
                read_stream(resp, f, use_tqdm)

            res = save_folder / file_name
    except FileIncompleteError as e:
        if save_folder is not None:
            logger.info(f"Deleting incomplete file {(save_folder / file_name)}")
            (save_folder / file_name).unlink()
        raise FileIncompleteError(f"Cannot download {model_id}") from e

    logger.info(f"Download of {model_id} successful")

    return res


def read_stream(resp: HTTPResponse, stream, use_tqdm):
    total_size = int(resp.headers.get('content-length', 0))

    with tqdm(total=total_size, unit='iB', unit_scale=True, disable=not use_tqdm, unit_divisor=1024) as t:
        remaining = total_size

        for block in resp.stream(32768):
            remaining -= len(block)
            t.update(len(block))
            stream.write(block)

    if remaining > 0:
        raise FileIncompleteError(f"Missing {remaining} Bytes")


def get_all_models(token: str, client: Optional[ApiClient] = None) -> List[Model]:
    total = -1
    models = []
    model_api = ModelAdminApi(client)
    status_code = None
    while len(models) < total or total < 0:
        try:
            resp, status_code, headers = model_api.admin_get_models_with_http_info(token, offset=len(models))
        except ApiException as e:
            if e.status == 404:
                logger.warning("API return a 404, maybe because the URl is wrong or because there is no model available")
            return []

        if status_code != 200:
            raise Exception(f'GET {resp.url} FAILED: {status_code}')

        firstlast, total = headers["Content-Range"].split("/")
        total = int(total)
        logger.info(f"Model pagination: {len(models)}/{total}")

        models.extend(resp)
    logger.info(f"Models found: {len(models)}")
    if len(models) != total:
        raise Exception(f'Receive more or less data than expected : {len(models)} instead of {total}')
    return models

def get_all_application(token: str, client: Optional[ApiClient] = None) -> List[Model]:
    total = -1
    models = []
    application_api = ApplicationAdminApi(client)
    status_code = None
    while len(models) < total or total < 0:
        try:
            resp, status_code, headers = application_api.admin_get_applications_with_http_info(token, offset=len(models))
        except ApiException as e:
            if e.status == 404:
                logger.warning("API return a 404, maybe because the URl is wrong or because there is no application available")
            return []

        if status_code != 200:
            raise Exception(f'GET {resp.url} FAILED: {status_code}')

        firstlast, total = headers["Content-Range"].split("/")
        total = int(total)
        logger.info(f"Model pagination: {len(models)}/{total}")

        models.extend(resp)
    logger.info(f"Models found: {len(models)}")
    if len(models) != total:
        raise Exception(f'Receive more or less data than expected : {len(models)} instead of {total}')
    return models

def download_models(token, save_folder: Optional[Union[Path, str]] = None, whitelist: Set[str] = (), blacklist: Set[str] = (), overwrite: bool = False,
                    use_tqdm: bool = True, keep_model: bool = True, stop_if_error: bool = False, client: Optional[ApiClient] = None,
                    fn_subfolder: Callable[[Application, Model], Union[str, Path]] = lambda application, model: application.application_name,
                    fn_filename: Callable[[Union[Model, Tuple[str, str], Tuple[str, str, Optional[int]]]], Union[str, Path]] = lambda model: f"{model.name}.model"):
    # if len(whitelist) > 0 and len(blacklist) > 0:
    #     raise ValueError("whitelist and blacklist cannot be set at the same time")

    applications: Dict[str, Application] = {app.id: app for app in get_all_application(token, client)}
    print(applications.keys())
    models: List[Model] = get_all_models(token=token, client=client)

    if save_folder is not None:
        if not isinstance(save_folder, Path):
            save_folder = Path(save_folder)

    if whitelist:
        models = [model for model in models if len({model.name, model.short_name, model.id, model.md5sum}.intersection(whitelist)) > 0]
    if blacklist:
        models = [model for model in models if len({model.name, model.short_name, model.id, model.md5sum}.intersection(blacklist)) == 0]

    for model in models:
        try:
            if save_folder is not None:
                folder = save_folder / fn_subfolder(applications[model.application_id], model)
            else:
                folder = None
            file = download_model(token=token, model=model, save_folder=folder, overwrite=overwrite, use_tqdm=use_tqdm, client=client, fn_filename=fn_filename)
            if file is None:
                continue
            try:
                yield model, file
            finally:
                if not keep_model:
                    file.unlink()
        except FileIncompleteError as e:
            logger.exception(f"Cannot download model {model.name} - {model.id} - {model.short_name}")
            if stop_if_error:
                raise
        except Exception as e:
            logger.exception("")
            if stop_if_error:
                raise
