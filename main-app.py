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
    '''
        Handles the add link request
    '''
    link_raw = request.form['text']

    # Parse input
    # input is expected to be: $title; $url; $tag1, $tag2; 
    try:
        (title, url, tags) = link_raw.split(';')[0:3]
        tags = tags.split(',')
        link_dict.add_link(title,url,tags)

    except Exception:
        err_str = '''It looks like you have an error in your reqeust.
                Make sure you follow the format: \"$title; $url; $tag1, $tag2;\" and ensure that the url you passed is valid
            '''
        return err_str, 400
    return "Link added successfully!"

http_server = WSGIServer(('', 80), app)
http_server.serve_forever()
