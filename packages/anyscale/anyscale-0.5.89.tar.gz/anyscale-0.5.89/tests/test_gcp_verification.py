from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import re
from threading import Thread
from typing import Any, Callable, Dict, List, Optional, Tuple
from unittest.mock import patch

from google.api_core.exceptions import NotFound
from google.auth.credentials import AnonymousCredentials
from googleapiclient.errors import HttpError
import pytest

from anyscale.cli_logger import BlockLogger
from anyscale.gcp_verification import GoogleCloudClientFactory, verify_gcp


class RequestTracker:
    def __init__(self):
        self.responses: Dict[str, List[Tuple[int, Optional[str]]]] = {}
        self.seen_requests: List[Any] = []

    def reset(self, responses):
        self.responses = responses
        self.seen_requests = []


class GCloudMockHandler(BaseHTTPRequestHandler):
    def __init__(self, tracker, *args, **kwargs):
        self.tracker = tracker
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.tracker.seen_requests.append(self.request)
        for regex in self.tracker.responses:
            if re.match(regex, self.path):
                code, body_file = self.tracker.responses[regex].pop(0)

                self.send_response(code)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                if body_file is not None:
                    with open(
                        Path(__file__).parent.joinpath("gcp_responses", body_file)
                    ) as f:
                        self.wfile.write(json.dumps(json.load(f)).strip().encode())
                        return

                return

        # Fail if nothing matches a request
        pytest.fail(
            f"Un handled request to {self.path}:\n{self.tracker.responses}",
            pytrace=False,
        )


@pytest.fixture()
def setup_mock_server() -> Tuple[GoogleCloudClientFactory, RequestTracker]:
    tracker = RequestTracker()

    server = HTTPServer(("localhost", 0), partial(GCloudMockHandler, tracker))
    port = server.server_address[1]
    print(f"Serving on (http://localhost:{port})")
    t = Thread(target=server.serve_forever, daemon=True)
    t.start()
    return (
        GoogleCloudClientFactory(
            credentials=AnonymousCredentials(),
            force_rest=True,
            client_options={"api_endpoint": f"http://127.0.0.1:{port}"},
        ),
        tracker,
    )


@pytest.mark.parametrize(
    "call_factory",
    [
        pytest.param(
            lambda f: f.compute_v1.NetworksClient().get(project="abc", network="cde"),
            id="Compute",
        ),
        pytest.param(
            lambda f: f.resourcemanager_v3.ProjectsClient().get_project(
                name="projects/abc"
            ),
            id="ResourceManager",
        ),
    ],
)
def test_client_factory_cloud_client(setup_mock_server, call_factory: Callable):
    factory, tracker = setup_mock_server
    tracker.reset(responses={".*": [(404, None)]})
    with pytest.raises(NotFound):
        call_factory(factory)


def test_client_factory_apis(setup_mock_server):
    factory, tracker = setup_mock_server
    tracker.reset(responses={".*": [(417, None)]})

    with pytest.raises(HttpError) as e:
        factory.build("iam", "v1").projects().serviceAccounts().get(
            name="projects/-/serviceAccounts/abc"
        ).execute()
    assert e.value.status_code == 417


@pytest.mark.parametrize("projects_match", [True, False])
def test_gcp_verify_credentials_project(capsys, projects_match: bool):
    project = "gcp_project"

    credentials_project = project if projects_match else "other_gcp_project"
    with patch(
        "anyscale.gcp_verification.get_application_default_credentials"
    ) as mock_credentials:
        mock_credentials.return_value = (
            AnonymousCredentials(),
            credentials_project,
        )
        assert verify_gcp({"project_id": project}, BlockLogger())
        mock_credentials.assert_called_once()

    _, err = capsys.readouterr()
    assert ("Default credentials are for" in err) != projects_match
