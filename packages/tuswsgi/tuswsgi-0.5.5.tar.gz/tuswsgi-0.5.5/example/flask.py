from flask import Flask
from tuswsgi import TusMiddleware

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
