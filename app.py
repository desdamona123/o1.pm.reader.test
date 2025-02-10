# app.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    # By default, runs on http://127.0.0.1:5000
    app.run()