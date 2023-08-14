# Use the official Python base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container's working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container's working directory
COPY . .
 
# Expose port 5000 for the Flask web application
EXPOSE 5000

# Command to run the Python web application
CMD ["python", "app.py"]
