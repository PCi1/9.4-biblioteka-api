import json
from os import name
from flask import Flask, jsonify, abort, request
from models import books, authors
from flask import make_response

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

#lista wszystkich książek
@app.route("/api/v1/books/", methods=["GET"])
def books_list_api_v1():
    return jsonify(books.all())

#lista wszystkich autorów
@app.route("/api/v1/authors/", methods=["GET"])
def authors_list_api_v1():
    return jsonify(authors.all())

#wybrana książka
@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({'book':book})

#wybrany autor
@app.route('/api/v1/authors/<int:author_id>', methods=["GET"])
def get_author(author_id):
    author = authors.get(author_id)
    if not author:
        abort(404)
    return jsonify({'author': author})

#dodanie książki
@app.route('/api/v1/books/', methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        abort(400)
    book = {
        'id': books.all()[-1]['id'] +1,
        'title': request.json['title'],
        'author': request.json['author'],
        'length': request.json.get('length', 0),
        'read': request.json.get('read', False)
    }
    books.create(book)
    return jsonify({'book': book}), 201

#dodanie autora
@app.route('/api/v1/authors/', methods=['POST'])
def create_author():
    if not request.json or not 'first_name' in request.json or not 'last_name' in request.json:
        abort(400)
    author = {
        'id':authors.all()[-1]['id'] +1,
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name'],
        'books': request.json.get('books', [])
    }
    authors.create(author)
    return jsonify({'author': author}), 201

#usunięcie książki
@app.route('/api/v1/books/<int:book_id>', methods = ['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result':result})

#usunięcie autora
@app.route('/api/v1/authors/<int:author_id>', methods = ['DELETE'])
def delete_author(author_id):
    result = authors.delete(author_id)
    if not result:
        abort(404)
    return jsonify({'result':result})

#nadpisanie książki
@app.route('/api/v1/books/<int:book_id>', methods = ['PUT'])
def update_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'length' in data and not isinstance(data.get('length'), int),
        'read' in data and not isinstance(data.get('read'), bool)

    ]):
        abort(400)
    book = {
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'length': data.get('length', book['length']),
        'read':data.get('read', book['read'])
    }
    books.update(book_id, book)
    return jsonify({'book': book})

#nadpisanie autora
@app.route('/api/v1/authors/<int:author_id>', methods = ['PUT'])
def update_author(author_id):
    author = authors.get(author_id)
    if not author:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'first_name' in data and not isinstance(data.get('first_name'), str),
        'last_name' in data and not isinstance(data.get('last_name'), str),
        'books' in data and not isinstance(data.get('books'), list)
    ]):
        abort(400)
    author = {
        'first_name': data.get('first_name', author['first_name']),
        'last_name': data.get('last_name', author['last_name']),
        'books': data.get('books', author['books'])
    }
    authors.update(author_id, author)
    return jsonify({'author': author})

#najdłuższa książka
@app.route('/api/v1/books/longest_book', methods = ['GET'])
def longest_book():
    return jsonify(books.longest_book())

#autor z największą ilością książek
@app.route('/api/v1/authors/most_titles', methods = ['GET'])
def most_titles():
    return jsonify(authors.most_titles())

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code':404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error':'Bad Request', 'status_code':'400'}),400)

if __name__ == "__main__":
    app.run(debug=True)