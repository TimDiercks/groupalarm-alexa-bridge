# Use official lightweight Python image
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose the port your app listens on
EXPOSE 5000

# Run Gunicorn with 4 workers, binding to 0.0.0.0:5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
