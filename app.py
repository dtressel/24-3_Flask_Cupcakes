from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'fruitsmell9753'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/api/cupcakes')
def return_all_cupcakes():
    """Returns a json object with all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes = serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def return_cupcake_by_id(cupcake_id):
    """Returns a json object with info about a particular cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake = serialized)

@app.route('/api/cupcakes', methods = ['POST'])
def add_new_cupcake():
    """Adds a new cupcake to the database"""

    new_cupcake = Cupcake(
        flavor = request.json['flavor'],
        size = request.json['size'],
        rating = request.json['rating']
        )
    if request.json.get('image'):
        new_cupcake.image = request.json['image']
    db.session.add(new_cupcake)
    db.session.commit()
    res = jsonify(cupcake = new_cupcake.serialize())
    return (res, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ['PATCH'])
def update_cupcake(cupcake_id):
    """updates a cupcake in the database"""

    selected_cupcake = Cupcake.query.get_or_404(cupcake_id)
    if request.json.get('flavor'):
        selected_cupcake.flavor = request.json['flavor']
    if request.json.get('size'):
        selected_cupcake.size = request.json['size']
    if request.json.get('rating'):
        selected_cupcake.rating = request.json['rating']
    if request.json.get('image'):
        selected_cupcake.image = request.json['image']
    db.session.add(selected_cupcake)
    db.session.commit()
    return jsonify(cupcake = selected_cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ['DELETE'])
def delete_cupcake(cupcake_id):
    """deletes a cupcake in the database"""

    selected_cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(selected_cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

@app.route('/')
def show_home():
    """shows home page"""

    return render_template('home.html')