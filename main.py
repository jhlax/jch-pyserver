import os

from flask import Flask

app = Flask(__name__)
# Comment below for production.
app.config['DEBUG'] = True


@app.route('/')
def index():
    return 'SOFTMAX.LIVE'


if __name__ == '__main__':
    app.run('0.0.0.0', port=os.environ['PORT'])  # get the port from the environment
                                                 # due to Heroku's limitations on such things
