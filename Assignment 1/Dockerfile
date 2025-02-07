# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app.py file into the container
COPY app.py /app/

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
