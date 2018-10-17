from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Success.'


if __name__ == '__main__':
    app.run(port=80)
