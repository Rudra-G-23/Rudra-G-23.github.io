# Use the slim base image
FROM python:3.10

# Set the folder inside the container where your code will live
WORKDIR /code

# Copy the requirements file first (better for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy your main.py into the container
COPY main.py .

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]