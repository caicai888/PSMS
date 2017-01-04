#!/usr/bin/env python
# coding=utf-8
from main import create_app

config = "default"
app = create_app(config)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555)

