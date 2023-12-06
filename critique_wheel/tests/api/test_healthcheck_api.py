import pytest
import requests

from critique_wheel import config


@pytest.mark.usefixtures("restart_api")
def test_healthcheck_api_returns_ok():
    url = config.get_api_url()

    response = requests.get(f"{url}/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
