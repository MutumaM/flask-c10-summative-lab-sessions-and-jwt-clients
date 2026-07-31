from config import app, db
from models import User, Note

with app.app_context():
    print("Clearing existing data...")
    Note.query.delete()
    User.query.delete()

    print("Seeding users...")
    user1 = User(username="alice")
    user1.password_hash = "password123"

    user2 = User(username="bob")
    user2.password_hash = "password456"

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Seeding notes...")
    note1 = Note(title="Grocery list", content="Milk, eggs, bread", user_id=user1.id)
    note2 = Note(title="Meeting notes", content="Discuss Q3 roadmap", user_id=user1.id)
    note3 = Note(title="Workout plan", content="Legs on Monday", user_id=user2.id)

    db.session.add_all([note1, note2, note3])
    db.session.commit()

    print("Seeding complete!")