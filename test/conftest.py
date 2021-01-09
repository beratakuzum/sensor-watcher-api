import pytest
import os

from app_setup import create_app


@pytest.fixture(scope="session")
def app():
    # create the app instance
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()
    return app
