from pymongo import MongoClient
import re
import atexit

# Below is stolen from https://codereview.stackexchange.com/a/19670
URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# Create mongo client
client = MongoClient('localhost', 27017)
link_db = client['link_db']
link_coll = link_db['link']

def get_link(query):
    '''
        Searches the mongo database for the query term looking
        in keys "title" and "tags" and doing a .contains query
    '''
    query_regex = re.compile(query, re.IGNORECASE)
    result_stream = link_coll.find({'$or': [{'title':query_regex}, {'tags':query_regex}]})
    return [e for e in result_stream] # return as list so we can handle it

def add_link(title, link, tags):
    '''
        Adds the link to the database with the passed title and tags
    '''

    # Checking Parameters
    assert URL_REGEX.match(link) # make sure the link is a valid url
    if not isinstance(tags, list): # make sure that tags is an array otherwise make it one
        tags = [tags]
    tags = [str(e) for e in tags] # make sure the elements of tags are strings

    # Now add to DB
    link = {'link': link, 'title': title, 'tags': tags} # Dict for the object
    link_coll.insert_one(link) # Actual insertion

def cleanup():
    client.close()
atexit.register(cleanup)
