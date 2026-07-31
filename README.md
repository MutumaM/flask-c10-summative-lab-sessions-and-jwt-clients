# Notes API

A secure Flask backend for a personal notes app. Users sign up, log in, and manage their own notes — session-based authentication ensures no user can view or modify another user's notes.

## Description

- **Users** — register and log in with a username and password (hashed with Bcrypt, never stored in plain text)
- **Notes** — each note has a `title`, `content`, and belongs to exactly one user via `user_id`

### Auth Routes

| Method | Route | Description |
|---|---|---|
| POST | `/signup` | Create an account and log in |
| POST | `/login` | Log in with username/password |
| DELETE | `/logout` | Log out (clears session) |
| GET | `/check_session` | Check if a user is currently logged in |

### Notes Routes (require login)

| Method | Route | Description |
|---|---|---|
| GET | `/notes` | List the logged-in user's notes, paginated (`?page=1&per_page=5`) |
| POST | `/notes` | Create a note |
| PATCH | `/notes/<id>` | Update a note (only if it belongs to you) |
| DELETE | `/notes/<id>` | Delete a note (only if it belongs to you) |

Every notes route checks, in order: is someone logged in (`401` if not), does the note exist (`404` if not), does it belong to the logged-in user (`403` if not).

## Requirements

- Python 3.8.13+
- Pip, Git

## Installation

```bash
git clone <your-repo-url>
cd flask-c10-summative-lab-sessions-and-jwt-clients
python3 -m venv .venv
source .venv/bin/activate
pip install flask==2.2.2 flask-sqlalchemy==3.0.3 werkzeug==2.2.2 marshmallow==3.20.1 faker==15.3.2 flask-migrate==4.0.0 flask-restful==0.3.9 importlib-metadata==6.0.0 importlib-resources==5.10.0 pytest==7.2.0 flask-bcrypt==1.0.1

cd server
flask db init
flask db migrate -m "create users and notes tables"
flask db upgrade
python seed.py
```

## Running

From `server/`:

```bash
python app.py
```

API runs at `http://localhost:5555`. Test with Thunder Client or `curl` — remember to send JSON bodies with the `Content-Type: application/json` header for POST/PATCH requests.

To use the provided frontend instead, run the sessions client in a second terminal:

```bash
cd client-with-sessions
npm install
npm start
```

## Seeded Test Accounts

| Username | Password |
|---|---|
| alice | password123 |
| bob | password456 |
