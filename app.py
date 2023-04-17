from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
# client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017, username='username', password='password')

client = MongoClient("mongodb+srv://Nikyar:SuperSmashBros1@cluster0.ch6oxtu.mongodb.net/?retryWrites=true&w=majority")
db = client.test


db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
# This takes the 'content' & 'degree' form requests filled by the user in the index web page and creates a todo with it
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@app.post('/<id>/delete/')  # @app.post is the equivalent of @app.route, adapted to accept only POST requests
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})  # This function search for any todo with an ObjectId id and deletes it
    return redirect(url_for('index'))

# This function search for any the todo with the ObjectId id and changes its degree to "Done" through update_one()
@app.post('/<id>/done/')
def done(id):
    todos.update_one({'_id' : ObjectId(id)}, {"$set": {'degree': "Done"}})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
