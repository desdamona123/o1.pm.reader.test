# run.py
from app import create_app  # This imports the create_app function from your app package

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)# Runs the Flask app