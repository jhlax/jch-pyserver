import os

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Success. 1-2-3.'


if __name__ == '__main__':
    app.run('0.0.0.0', port=os.environ['PORT'])
