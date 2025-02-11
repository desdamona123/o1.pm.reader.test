# run.py
from app import create_app  # This imports the create_app function from your app package

app = create_app()

if __name__ == '__main__':
    app.run()  # Runs the Flask app