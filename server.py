from pymongo.common import SERVER_SELECTION_TIMEOUT
from flask_mongoengine import MongoEngine
from flask import Flask, Response, request
from json import dumps
import mongoengine as me #could also be done with flask-mongoengine


app = Flask(__name__)
try:
    app.config["MONGODB_HOST"] = DB_URI
    app.config['MONGODB_SETTINGS'] = {
    "db" : "library",
    }
    db = MongoEngine(app)

except Exception as e:
    print("UNABLE TO CONNECT TO THE DATABASE")


class Book(me.Document):
    name = me.StringField(required=True)
    author = me.StringField()
    
    def to_json(self):
        return {
            "_id": str(self.pk),
            "name": self.name,
            "author": self.author,
        }

@app.route('/books/createBook', methods=['POST'])
def create():
    try:
        name = request.form["name"]
        author = request.form["author"]
        b1 = Book(name=str(name), author=str(author))
        b1.save()
        context = {
            "message": "The book was created successfully",
            "user" : b1.to_json() 
        }
        return Response(
            response = dumps(context),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        context = {
            "message": "could not complete the request",
        }
        return Response(
            response = dumps(context),
            status=500,
            mimetype="application/json"
        )
        
@app.route('/books/', methods=['GET'])
def read():
    try:
        all_books = Book.objects
        return Response(
            response = all_books.to_json(),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        context = {
            "message": "could not complete the request",
        }
        return Response(
            response = dumps(context),
            status=500,
            mimetype="application/json"
        )


@app.route('/books/<id>', methods=['PUT'])
def update(id):
    try:
        book = Book.objects.get(pk=id)
    except Exception as e:
        context = {
            "message" : "No such book found"
        }
        return Response(
        response =dumps(context),
        status=404,
        mimetype="application/json"
    )
    
    try:
        book.name = request.form["name"]
        book.author = request.form["author"]
        book.save()
        return Response(
            response =dumps({"message":"book updated"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        context = {
            "message": "could not complete the request",
        }
        return Response(
            response = dumps(context),
            status=500,
            mimetype="application/json"
        )

@app.route('/books/<id>', methods=['DELETE'])
def delete(id):
    try:
        book = Book.objects.get(pk=id)
    except Exception as e:
        context = {
            "message" : "No such book found"
        }
        return Response(
        response =dumps(context),
        status=404,
        mimetype="application/json"
        )

    try:
        book = Book.objects.get(pk=id)
        book.delete()
        context = {
            "message": "book has been deleted",
        }

        return Response(
            response = dumps(context),
            status=200,
            mimetype="application/json"
        )
    except:
        context = {
            "message": "could not complete the request",
        }
        return Response(
            response = dumps(context),
            status=500,
            mimetype="application/json"
        )


if __name__ == "__main__":
    app.run(debug=True, port=8081)
