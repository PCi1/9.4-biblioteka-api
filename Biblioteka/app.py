from flask import Flask, render_template, request, redirect, url_for

from forms import BookForm, AuthorForm, reload_authors
from models import books, authors

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

@app.route('/books/', methods=["GET", "POST"])
def books_list():
    form = BookForm()
    form2 = AuthorForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            books.create(form.data)
            books.save_all()
            authors.save_all()
        elif form2.validate_on_submit():
            authors.create(form2.data)
            authors.save_all()
            reload_authors()
        return redirect(url_for("books_list"))
    return render_template("books.html", form=form, form2=form2, books=books.all(), error=error)


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = books.get(book_id - 1)
    form = BookForm(data=book)
    if request.method == "POST":
        if form.validate_on_submit():
            books.update(book_id - 1, form.data)
        return redirect(url_for("books_list"))
    return render_template("book.html", form=form, book_id=book_id)


if __name__ == "__main__":
    app.run(debug=False)
