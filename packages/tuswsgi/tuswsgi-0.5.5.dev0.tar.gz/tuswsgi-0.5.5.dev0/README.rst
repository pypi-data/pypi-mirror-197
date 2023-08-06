=========
tusfilter
=========

python wsgi filter for tus protocol 1.0.0, `the tus resumable upload standard`_.

Fork of https://github.com/everydo/tusfilter with bugfixes for WebOb Request usage.

.. _the tus resumable upload standard: http://tus.io/


install
-------

::

    pip install tuswsgi


Arguments
---------

app
    required, the wsgi server application

upload_path
    ``str``, required, path of the upload service

tmp_dir
    ``str``, optional, directory to store temporary files, default ``/upload``

expire
    ``int``, optional, how long before cleanup old uploads in seconds, default ``60*60*60``

send_file
    ``bool``, optional, ``False`` for send the absolute filepath in ``tmp_dir`` in the request body,
    ``True`` for an actual file uploaded, default ``False``

max_size
    ``int``, optional, maximum size of uploads in bytes, default ``2**30``, 1G


Example
-------

flask ::

    from tuswsgi import TusMiddleware
    from flask import Flask

    app = Flask(__name__)

    @app.route("/upload_resumable/<tmpfile>", methods=['PATCH'])
    def upload_resumable(tmpfile):
        # do something else
        return 'End of upload'

    app.wsgi_app = TusMiddleware(
        app.wsgi_app,
        upload_path='/upload_resumable',
        tmp_dir='/tmp/upload',
    )
