# same as flask app used for debugging


from flask import send_from_directory
import os
from pymongo import MongoClient
from flask import Flask, render_template
import urllib.request
# import json
from utils import *

app = Flask(__name__)

author_list = [
    'J. K. Rowling',
    'Stephen King',
    'Gabriel Garcia Marquez'
]
auth_key_dict = {auth: return_auth_key(auth) for auth in author_list}


client = MongoClient('localhost', 27017)
db = client.bigdata_hw
collection = db.authors_final


@app.route('/')
def index():
    return render_template('index.html', author_key_dict=auth_key_dict)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<id>')
def author_page(id):
    print(id)
    auth_key = return_auth_key(id)
    print(auth_key)
    query = {"bio.key": f'/authors/{auth_key}'}
    # book_auth = collection.find(query)
    # for book in book_auth:
    #     print(book)
    author = collection.find(query)
    works_amazon = return_amazon_works(author)
    return render_template('author.html', id_author=collection.find(query), akey=auth_key, books_amazon=return_all_isbn(author), works_amazon=works_amazon)


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
