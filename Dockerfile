# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install the dependencies
# --no-cache-dir: Disables the pip cache to reduce image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application using Gunicorn
# This is a production-ready WSGI server.
# It assumes your main Flask file is 'app.py' and the Flask app instance is named 'app'.
# If your file is `main.py` and your app instance is `my_app`, you would change this to:
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:my_app"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
