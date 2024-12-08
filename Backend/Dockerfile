# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy backend files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask pandas scikit-learn imbalanced-learn joblib

# Expose port
EXPOSE 5000

# Set environment variable
ENV FLASK_APP=app.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
