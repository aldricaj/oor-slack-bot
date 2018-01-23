from flask import Flask
from flask import request
from gevent.wsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/slackapi/linkfor', methods=['POST'])
def handle_linkfor():
    data = request.form 
    print(data['text'])

http_server = WSGIServer(('', 80), app)
http_server.serve_forever()
