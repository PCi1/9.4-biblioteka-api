import json


class Books:
    def __init__(self):
        try:
            with open("books.json", "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, id):
        book = [book for book in self.all() if book["id"] == id]
        if book:
            return book[0]
        return []

    def create(self, data):
        self.books.append(data)
        self.save_all()

    def save_all(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        book = self.get(id)
        if book:
            index = self.books.index(book)
            self.books[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        book = self.get(id)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False
    
    def longest_book(self):
        book = self.books[0]
        for i in self.books:
            if i.get('length') > book.get('length'):
                book = i
        return book

books = Books()

class Authors:
    def __init__(self):
        try:
            with open("authors.json", 'r') as f:
                self.authors = json.load(f)
        except FileNotFoundError:
            self.authors = []
    
    def all(self):
        return self.authors

    def get(self, id):
        author = [author for author in self.all() if author['id'] == id]
        if author:
            return author[0]
        else:
            return []

    def create(self, data):
        self.authors.append(data)
        self.save_all()
    
    def save_all(self):
        with open("authors.json", "w") as f:
            json.dump(self.authors, f)

    def update(self, id, data):
        author = self.get(id)
        if author:
            index = self.authors.index(author)
            self.authors[index] - data
            self.save_all()
            return True
        return False

    def delete(self, id):
        author = self.get(id)
        if author: 
            self.authors.remove(author)
            self.save_all()
            return True
        return False

    def most_titles(self):
        author = self.authors[0]
        for i in self.authors:
            if len(i.get('books')) > len(author.get('books')):
                author = i
        return author


authors = Authors()