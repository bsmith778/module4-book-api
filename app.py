from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "book_name": self.book_name,
            "author": self.author,
            "publisher": self.publisher
        }

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Book API is running!"})

# CREATE - add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "book_name" not in data or "author" not in data or "publisher" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_book = Book(
        book_name=data["book_name"],
        author=data["author"],
        publisher=data["publisher"]
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify(new_book.to_dict()), 201

# READ - get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

# READ - get one book by id
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book.to_dict())

# UPDATE - update a book by id
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    book.book_name = data.get("book_name", book.book_name)
    book.author = data.get("author", book.author)
    book.publisher = data.get("publisher", book.publisher)

    db.session.commit()

    return jsonify(book.to_dict())

# DELETE - delete a book by id
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"})

# Create the database tables
with app.app_context():
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)