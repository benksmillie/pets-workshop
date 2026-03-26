import os
from typing import Dict, List, Any, Optional, Union, Tuple
from flask import Flask, jsonify, Response
from flask_cors import CORS
from models import init_db, db, Dog, Breed

# Get the server directory path
base_dir: str = os.path.abspath(os.path.dirname(__file__))

app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "dogshelter.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Initialize the database with the app
init_db(app)

@app.route('/api/dogs', methods=['GET'])
def get_dogs() -> Response:
    """
    Get all dogs with optional filtering by breed and availability status.
    
    Query Parameters:
        breed (str, optional): Filter by breed name
        available (bool, optional): Filter by availability (true/false)
    
    Returns:
        Response: JSON list of dogs
    """
    from flask import request
    from models.dog import AdoptionStatus
    
    query = db.session.query(
        Dog.id, 
        Dog.name, 
        Breed.name.label('breed'),
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id)
    
    # Apply breed filter if provided
    breed_filter: Optional[str] = request.args.get('breed')
    if breed_filter:
        query = query.filter(Breed.name == breed_filter)
    
    # Apply availability filter if provided
    available_filter: Optional[str] = request.args.get('available')
    if available_filter and available_filter.lower() == 'true':
        query = query.filter(Dog.status == AdoptionStatus.AVAILABLE)
    
    dogs_query = query.all()
    
    # Convert the result to a list of dictionaries
    dogs_list: List[Dict[str, Any]] = [
        {
            'id': dog.id,
            'name': dog.name,
            'breed': dog.breed
        }
        for dog in dogs_query
    ]
    
    return jsonify(dogs_list)

@app.route('/api/dogs/<int:id>', methods=['GET'])
def get_dog(id: int) -> Union[Tuple[Response, int], Response]:
    # Query the specific dog by ID and join with breed to get breed name
    dog_query = db.session.query(
        Dog.id,
        Dog.name,
        Breed.name.label('breed'),
        Dog.age,
        Dog.description,
        Dog.gender,
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id).filter(Dog.id == id).first()
    
    # Return 404 if dog not found
    if not dog_query:
        return jsonify({"error": "Dog not found"}), 404
    
    # Convert the result to a dictionary
    dog: Dict[str, Any] = {
        'id': dog_query.id,
        'name': dog_query.name,
        'breed': dog_query.breed,
        'age': dog_query.age,
        'description': dog_query.description,
        'gender': dog_query.gender,
        'status': dog_query.status.name
    }
    
    return jsonify(dog)

@app.route('/api/breeds', methods=['GET'])
def get_breeds() -> Response:
    """
    Get all available dog breeds.
    
    Returns:
        Response: JSON list of breeds with id and name
    """
    # Query all breeds
    breeds_query = db.session.query(Breed.id, Breed.name).all()
    
    # Convert the result to a list of dictionaries
    breeds_list: List[Dict[str, Any]] = [
        {
            'id': breed.id,
            'name': breed.name
        }
        for breed in breeds_query
    ]
    
    return jsonify(breeds_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
