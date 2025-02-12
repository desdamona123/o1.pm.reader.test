# 1. Start with a lightweight Python base image:
FROM python:3.9-slim

# 2. Create a folder inside the container to hold your app's files.
WORKDIR /app

# 3. Copy your Python requirements file and install packages.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy all the remaining code from your project into the container.
COPY . .

# 5. Set environment variables telling Flask how to run.
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# 6. Expose port 5000 so Cloud Run (or local Docker) can forward traffic.
EXPOSE 5000

# 7. Command to run your Flask app when the container starts:
CMD ["flask", "run"]