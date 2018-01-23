from flask import Flask
from flask import request
from gevent.wsgi import WSGIServer
import link_dict

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/slackapi/linkfor', methods=['POST'])
def handle_linkfor():
    data = request.form 
    links = link_dict.get_link(data['text'])

    return_text = 'Links mathching \"{}\" include: \n'.format(data['text']) 
    for link in links:
        return_text += '{}: {} \n'.format(link['title'], link['link'])

    return return_text

@app.route('/slackapi/addlink', methods=['POST'])
def handle_addlink():
    pass

http_server = WSGIServer(('', 80), app)
http_server.serve_forever()
