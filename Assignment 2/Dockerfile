# Step 1: Use an official Python runtime as the base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Install the necessary dependencies

RUN pip install --no-cache-dir --upgrade -r requirements.txt


# Step 5: Expose a port if needed (optional)
EXPOSE 5000

# Step 6: Define the environment variable (optional)
ENV PYTHONUNBUFFERED=1

# Step 7: Define the command to run your application
CMD ["python", "app.py"]
