from functools import partial
from typing import Any, Dict

from google.auth.credentials import Credentials
import google.cloud
from google.cloud import compute_v1, resourcemanager_v3  # noqa
from googleapiclient.discovery import build as api_client_build

from anyscale.cli_logger import BlockLogger
from anyscale.utils.gcp_utils import get_application_default_credentials


class GCPLogger:
    def __init__(self, logger: BlockLogger, project_id: str):
        self.internal = logger
        self.project_id = project_id

    def log_resource_not_found_error(self, resource_name: str, resource_id: str):
        self.internal.error(
            f"Could not find {resource_name} with id {resource_id} in project {self.project_id}. Please validate that you're using the correct GCP project and that the resource values are correct."
        )


class GoogleCloudClientFactory:
    """Factory to generate both Google Cloud Client libraries & Google API Client libraries.

    Google Cloud Client libraries are instantiated by:
    ```
        factory = GoogleCloudClientFactory(credentials=AnonymousCredentials())
        client = factory.compute_v1.ExampleClient()
    ```

    Google API Client libraries are instantiated by:
    ```
        factory = GoogleCloudClientFactory(credentials=AnonymousCredentials())
        client = factory.build("iam", v1")
    ```
    """

    def __init__(self, credentials: Credentials, force_rest=False, **kwargs):
        kwargs["credentials"] = credentials
        self.kwargs = kwargs
        self.force_rest = force_rest

    def __getattr__(self, client_library: str):
        """Get a wrapped Google Cloud Client library that injects default values from the factory."""
        module = getattr(google.cloud, client_library)
        kwargs = self.kwargs
        if self.force_rest:
            kwargs["transport"] = "rest"

        class WrappedClient:
            def __getattr__(self, client_type: str):
                return partial(getattr(module, client_type), **kwargs)

        return WrappedClient()

    def build(self, service_name: str, version: str):
        """Return a Google API Client with default values from the factor"""
        return api_client_build(
            service_name, version, cache_discovery=False, **self.kwargs
        )


def verify_gcp(resources: Dict[str, Any], logger: BlockLogger) -> bool:
    credentials, credentials_project = get_application_default_credentials(logger)
    specified_project = resources["project_id"]
    if credentials_project != specified_project:
        logger.warning(
            f"Default credentials are for {credentials_project}, but this cloud is being configured for {specified_project}"
        )

    GoogleCloudClientFactory(credentials=credentials)
    GCPLogger(logger, specified_project)
    return True
