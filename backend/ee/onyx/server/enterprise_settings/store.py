import os
from io import BytesIO
from typing import Any
from typing import cast
from typing import IO

from fastapi import HTTPException
from fastapi import UploadFile

from ee.onyx.configs.app_configs import WHITE_LABEL_APP_NAME
from ee.onyx.configs.app_configs import WHITE_LABEL_COMPANY_NAME
from ee.onyx.configs.app_configs import WHITE_LABEL_ENABLED
from ee.onyx.configs.app_configs import WHITE_LABEL_FAVICON_URL
from ee.onyx.configs.app_configs import WHITE_LABEL_FOOTER_BRANDING
from ee.onyx.configs.app_configs import WHITE_LABEL_LOGO_URL
from ee.onyx.configs.app_configs import WHITE_LABEL_PRIMARY_BRAND_COLOR
from ee.onyx.configs.app_configs import WHITE_LABEL_SUPPORT_EMAIL
from ee.onyx.configs.app_configs import WHITE_LABEL_SUPPORT_URL
from ee.onyx.server.enterprise_settings.models import AnalyticsScriptUpload
from ee.onyx.server.enterprise_settings.models import EnterpriseSettings
from onyx.configs.constants import FileOrigin
from onyx.configs.constants import KV_CUSTOM_ANALYTICS_SCRIPT_KEY
from onyx.configs.constants import KV_ENTERPRISE_SETTINGS_KEY
from onyx.configs.constants import ONYX_DEFAULT_APPLICATION_NAME
from onyx.file_store.file_store import get_default_file_store
from onyx.key_value_store.factory import get_kv_store
from onyx.key_value_store.interface import KvKeyNotFoundError
from onyx.utils.logger import setup_logger

logger = setup_logger()

_LOGO_FILENAME = "__logo__"
_LOGOTYPE_FILENAME = "__logotype__"


def load_settings() -> EnterpriseSettings:
    """Loads settings data directly from DB. This should be used primarily
    for checking what is actually in the DB, aka for editing and saving back settings.

    Runtime settings actually used by the application should be checked with
    load_runtime_settings as defaults may be applied at runtime.
    """

    dynamic_config_store = get_kv_store()
    try:
        settings = EnterpriseSettings(
            **cast(dict, dynamic_config_store.load(KV_ENTERPRISE_SETTINGS_KEY))
        )
    except KvKeyNotFoundError:
        settings = EnterpriseSettings()
        dynamic_config_store.store(KV_ENTERPRISE_SETTINGS_KEY, settings.model_dump())

    return settings


def store_settings(settings: EnterpriseSettings) -> None:
    """Stores settings directly to the kv store / db."""

    get_kv_store().store(KV_ENTERPRISE_SETTINGS_KEY, settings.model_dump())


def apply_white_label_overlay(settings: EnterpriseSettings) -> EnterpriseSettings:
    """Overlay env-var-driven branding on top of stored EnterpriseSettings.

    No-op unless WHITE_LABEL_ENABLED=true. For every WHITE_LABEL_* env var that
    is set, the corresponding field is overwritten on the returned object so
    env always wins over DB. Fields without a matching env var are left as-is,
    so admin UI edits to non-overridden fields keep working.

    Mutates `settings` in place and returns it for chaining convenience.
    """
    if not WHITE_LABEL_ENABLED:
        return settings

    if WHITE_LABEL_APP_NAME is not None:
        settings.application_name = WHITE_LABEL_APP_NAME
    if WHITE_LABEL_COMPANY_NAME is not None:
        settings.company_name = WHITE_LABEL_COMPANY_NAME
    if WHITE_LABEL_SUPPORT_EMAIL is not None:
        settings.support_email = WHITE_LABEL_SUPPORT_EMAIL
    if WHITE_LABEL_SUPPORT_URL is not None:
        settings.support_url = WHITE_LABEL_SUPPORT_URL
    if WHITE_LABEL_PRIMARY_BRAND_COLOR is not None:
        settings.primary_brand_color = WHITE_LABEL_PRIMARY_BRAND_COLOR
    if WHITE_LABEL_LOGO_URL is not None:
        settings.logo_url = WHITE_LABEL_LOGO_URL
    if WHITE_LABEL_FAVICON_URL is not None:
        settings.favicon_url = WHITE_LABEL_FAVICON_URL
    if WHITE_LABEL_FOOTER_BRANDING is not None:
        settings.footer_branding = WHITE_LABEL_FOOTER_BRANDING

    # The sidebar "Powered by ..." line interpolates application_name, so it
    # already reads correctly under white-label (e.g. "Powered by PDG Partners")
    # without needing to be force-hidden. Admins who want to drop the line
    # entirely can still flip hide_onyx_branding via the admin UI.

    return settings


def load_runtime_settings() -> EnterpriseSettings:
    """Loads settings from DB and applies any defaults or transformations for use
    at runtime.

    Should not be stored back to the DB.
    """
    enterprise_settings = load_settings()
    if not enterprise_settings.application_name:
        enterprise_settings.application_name = ONYX_DEFAULT_APPLICATION_NAME

    apply_white_label_overlay(enterprise_settings)

    return enterprise_settings


_CUSTOM_ANALYTICS_SECRET_KEY = os.environ.get("CUSTOM_ANALYTICS_SECRET_KEY")


def load_analytics_script() -> str | None:
    dynamic_config_store = get_kv_store()
    try:
        return cast(str, dynamic_config_store.load(KV_CUSTOM_ANALYTICS_SCRIPT_KEY))
    except KvKeyNotFoundError:
        return None


def store_analytics_script(analytics_script_upload: AnalyticsScriptUpload) -> None:
    if (
        not _CUSTOM_ANALYTICS_SECRET_KEY
        or analytics_script_upload.secret_key != _CUSTOM_ANALYTICS_SECRET_KEY
    ):
        raise ValueError("Invalid secret key")

    get_kv_store().store(KV_CUSTOM_ANALYTICS_SCRIPT_KEY, analytics_script_upload.script)


def is_valid_file_type(filename: str) -> bool:
    valid_extensions = (".png", ".jpg", ".jpeg")
    return filename.endswith(valid_extensions)


def guess_file_type(filename: str) -> str:
    if filename.lower().endswith(".png"):
        return "image/png"
    elif filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
        return "image/jpeg"
    return "application/octet-stream"


def upload_logo(file: UploadFile | str, is_logotype: bool = False) -> bool:
    content: IO[Any]

    if isinstance(file, str):
        logger.notice("Uploading logo from local path %s", file)
        if not os.path.isfile(file) or not is_valid_file_type(file):
            logger.error(
                "Invalid file type- only .png, .jpg, and .jpeg files are allowed"
            )
            return False

        with open(file, "rb") as file_handle:
            file_content = file_handle.read()
        content = BytesIO(file_content)
        display_name = file
        file_type = guess_file_type(file)

    else:
        logger.notice("Uploading logo from uploaded file")
        if not file.filename or not is_valid_file_type(file.filename):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type- only .png, .jpg, and .jpeg files are allowed",
            )
        content = file.file
        display_name = file.filename
        file_type = file.content_type or "image/jpeg"

    file_store = get_default_file_store()
    file_store.save_file(
        content=content,
        display_name=display_name,
        file_origin=FileOrigin.OTHER,
        file_type=file_type,
        file_id=_LOGOTYPE_FILENAME if is_logotype else _LOGO_FILENAME,
    )
    return True


def get_logo_filename() -> str:
    return _LOGO_FILENAME


def get_logotype_filename() -> str:
    return _LOGOTYPE_FILENAME
