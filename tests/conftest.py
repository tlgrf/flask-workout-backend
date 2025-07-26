import sys, os

# ensuring project root is on sys.path so `import server` works
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

from server.app import app as _app
from server.models import db
import pytest

@pytest.fixture
def app():
    _app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()