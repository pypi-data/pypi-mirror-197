import pytest
from flask import Flask
from tuswsgi import TusMiddleware



def create_app():
    app = Flask(__name__)

    @app.route("/upload_resumable/<tmpfile>", methods=['PATCH'])
    def upload_resumable(tmpfile):
        # do something else
        return 'End of upload'

    app.wsgi_app = TusMiddleware(
        app.wsgi_app,
        tmp_dir='/tmp/upload',
        upload_path='/upload_resumable',
    )
    return app


@pytest.fixture
def app():
    app = create_app()
    return app


# TODO extend this to some more meaningful tests
def test_app_constructed(client, app):
    res = client.post(
        '/upload_resumable/abc',
    )

    # Missing Tus-Resumable header
    assert res.status_code == 400
