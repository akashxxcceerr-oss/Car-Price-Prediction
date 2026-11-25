# wsgi.py — Production entry point for gunicorn / Render / Railway / etc.
# Imports the Flask app from main.py WITHOUT modifying main.py.
# gunicorn uses:  gunicorn wsgi:app

from main import app

if __name__ == "__main__":
    app.run()

