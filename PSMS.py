#!/usr/bin/env python
# coding=utf-8
from main import create_app
# from werkzeug.contrib.fixers import ProxyFix

config = "default"
app = create_app(config)
# app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555,threaded=True)

