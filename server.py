from flask import Flask, request, jsonify
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine 
from flask_sqlalchemy  import SQLAlchemy
import linked_list 

#app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQL_TRACK_MODIFICATIONS"] = 0

# Configure sqlite3 to enforce foreign key constraints, sql alchemy key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

db = SQLAlchemy(app)
now = datetime.now()

# models 
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")

class BlogPost(db.Model):
    __tablename__ = "blogpost"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# routes
@app.route("/user", methods=["POST"])
def create_user():
    # request provided by flask
    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()
    # response for request and 200
    return jsonify({"message": "User created"}), 200

@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    # gets data by descending order
    users = User.query.all()
    all_users_linked_list = linked_list.LinkedList()
    for user in users:
        all_users_linked_list.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
    return jsonify(all_users_linked_list.to_list()), 200

@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    # gets data by ascending order
    users = User.query.all()
    all_users_linked_list = linked_list.LinkedList()
    for user in users:
        all_users_linked_list.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
    return jsonify(all_users_linked_list.to_list()), 200

@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()
    all_users_linked_list = linked_list.LinkedList()
    for user in users:
        all_users_linked_list.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
    user = all_users_linked_list.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return "User Does not Exist", 404

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return "User Does not Exist", 404
    db.session.delete(user)
    db.session.commit()
    deleted_user = {
        "status": f"{user.name} has been deleted",
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "address": user.address,
        "phone": user.phone,
    }
    if user:
        return jsonify(deleted_user), 200
    

@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    pass

@app.route("/user/<user_id>", methods=["GET"])
def get_all_blog_posts(user_id):
    pass

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    pass

@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    pass

if __name__ == "__main__":
    app.run(debug=True)