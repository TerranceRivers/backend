import collections
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img_urlOne = db.Column(db.String,  unique=True)
    img_urlTwo = db.Column(db.String,  unique=True)
    img_urlThree = db.Column(db.String,  unique=False)
    amount = db.Column(db.Integer,  unique=False)
  

    def __init__(self, description, name, price, img_urlOne, img_urlTwo, img_urlThree, amount):
        self.name = name
        self.description = description
        self.price = price
        self.img_urlOne = img_urlOne
        self.img_urlTwo = img_urlTwo
        self.img_urlThree = img_urlThree
        self.amount = amount
      


class CollectionSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "description", "img_urlOne","img_urlTwo", "img_urlThree", "amount")


collection_schema = CollectionSchema()
multiple_collection_schema = CollectionSchema(many=True)


@app.route("/collection/add", methods=["POST"])
def add_collection():
    post_data = request.get_json()
    name = post_data.get("name")
    price = post_data.get("price")
    description = post_data.get("description")
    img_urlOne = post_data.get("img_urlOne")
    img_urlTwo = post_data.get("img_urlTwo")
    img_urlThree = post_data.get("img_urlThree")
    amount = post_data.get("amount")
 

    new_record = Collection(description, name, price, img_urlOne, img_urlTwo, img_urlThree, amount )
    db.session.add(new_record)
    db.session.commit()

    return jsonify("collection item added successfully")


@app.route("/collection/all", methods=["GET"])
def get_all_CollectionItems():
    records = db.session.query(Collection).all()
    return jsonify(multiple_collection_schema.dump(records))


@app.route("/collection/get/<name>", methods=['GET'])
def get_items_by_type(name):
    records = db.session.query(Collection).filter(
        Collection.name == name).all()
    return jsonify(collection_schema.dump(records))


@app.route("/collection/<id>", methods=["GET"])
def get_collection(id):
    records = db.session.query(Collection).filter(Collection.id == id).first()
    return (collection_schema.jsonify(records), "200")


@app.route('/collection/<id>', methods=['DELETE'])
def delete_collection(id):
    response = {}
    get_delete = Collection.query.get(id)
    response['id'] = get_delete.id
    db.session.delete(get_delete)
    db.session.commit()
    return jsonify(collection_schema(delete_collection), "collection was deleted")


@app.route('/collection/edit/<id>', methods=['PUT'])
def edit_collection(id):
    if request.content_type != 'application/json':
        return jsonify('This information needs to be sent as JSON smart guy!!')

    put_data = request.get_json()
    name = put_data.get('name')
    price = put_data.get('price')
    description = put_data.get('description')
    img_urlOne = put_data.get('img_urlOne')
    img_urlTwo = put_data.get('img_urlTwo')
    img_urlThree = put_data.get('img_urlThree')
    amount = put_data.get('amount')
   
   

    edit_collection = db.session.query(
        Collection).filter(Collection.id == id).first()

    if name != None:
        edit_collection.name = name
    if price != None:
        edit_collection.price = price
    if description != None:
        edit_collection.description = description
    if img_urlOne != None:
        edit_collection.img_url = img_urlOne
    if img_urlTwo != None:
        edit_collection.img_urlTwo = img_urlTwo
    if img_urlThree != None:
        edit_collection.img_urlThree = img_urlThree
    if img_urlThree != None:
        edit_collection.amount = amount
   

    db.session.commit()

    return jsonify(collection_schema.dump(edit_collection), "collection was edited")


@app.route('/collection/add/many', methods=["POST"])
def add_many_collection():
    if request.content_type != 'application/json':
        return jsonify("Error")

    post_data = request.get_json()
    collection = post_data.get('collection')

    new_records = []

    for collection in collections:
        name = collection.get('name')
        description = collection.get('description')
        price = collection.get('price')
        img_urlOne = collection.get('img_urlOne')
        img_urlTwo = collection.get('img_urlTwo')
        img_urlThree = collection.get('img_urlThree')
        amount = collection.get('amount')
     

        existing_collection_check = db.session.query(
            Collection).filter(Collection.name == name).first()
        if existing_collection_check is not None:
            return jsonify('')
        else:
            new_record = Collection(name, description, price, img_urlOne, img_urlTwo, img_urlThree, amount)
            db.session.add(new_record)
            db.session.commit()
            new_records.append(new_record)

    return jsonify(multiple_collection_schema.dump(new_records))


if __name__ == "__main__":
    app.run(debug=True)