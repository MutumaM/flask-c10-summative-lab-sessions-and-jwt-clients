from flask import request, session, jsonify
from config import app, db, api
from models import User, Note
from schemas import user_schema, note_schema, notes_schema


# Auth routes 

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Check the username isn't already taken
    existing = User.query.filter_by(username=data['username']).first()
    if existing:
        return jsonify({'error': 'Username already taken'}), 400

    try:
        new_user = User(username=data['username'])
        new_user.password_hash = data['password']  
        db.session.add(new_user)
        db.session.commit()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # Log the new user in immediately by storing their id in the session
    session['user_id'] = new_user.id

    return jsonify(user_schema.dump(new_user)), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if user and user.authenticate(data.get('password', '')):
        session['user_id'] = user.id
        return jsonify(user_schema.dump(user)), 200

    return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/logout', methods=['DELETE'])
def logout():
    session['user_id'] = None
    return {}, 204


@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return jsonify(user_schema.dump(user)), 200

    return jsonify({'error': 'Not logged in'}), 401


# Helper: require login for resource routes 

def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


# Notes routes 

@app.route('/notes', methods=['GET'])
def get_notes():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)


    query = Note.query.filter_by(user_id=user.id).order_by(Note.id.desc())


    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'notes': notes_schema.dump(paginated.items),
        'total': paginated.total,
        'page': paginated.page,
        'pages': paginated.pages
    }), 200


@app.route('/notes', methods=['POST'])
def create_note():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    errors = note_schema.validate(data, partial=('user_id',))
    if errors:
        return jsonify(errors), 400

    try:
        new_note = Note(
            title=data['title'],
            content=data['content'],
            user_id=user.id  
        )
        db.session.add(new_note)
        db.session.commit()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(note_schema.dump(new_note)), 201


@app.route('/notes/<int:id>', methods=['PATCH'])
def update_note(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    note = Note.query.get(id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    if note.user_id != user.id:
        return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json()
    try:
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']
        db.session.commit()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(note_schema.dump(note)), 200


@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    note = Note.query.get(id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    if note.user_id != user.id:
        return jsonify({'error': 'Forbidden'}), 403

    db.session.delete(note)
    db.session.commit()
    return {}, 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)