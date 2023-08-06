import subprocess
from typing import Optional, Tuple

import google.auth
from google.auth.credentials import Credentials

from anyscale.cli_logger import BlockLogger


def get_application_default_credentials(
    logger: BlockLogger,
) -> Tuple[Credentials, Optional[str]]:
    """Get application default credentials, or run `gcloud` to try to log in."""
    try:
        return google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError as e:
        logger.warning(
            "Could not automatically determine Google Application Default Credentials, trying to authenticate via GCloud"
        )
        auth_login = subprocess.run(["gcloud", "auth", "application-default", "login"])
        if auth_login.returncode != 0:
            raise RuntimeError("Failed to authenticate via gcloud") from e

        return google.auth.default()
