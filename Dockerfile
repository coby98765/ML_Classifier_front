# Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose default Streamlit port
EXPOSE 8501

# Set environment variable for backend URL (can also be set via docker run)
ENV BACKEND_URL=http://localhost:8001

# Launch app
CMD ["streamlit", "run", "Home.py", "--server.headless=true", "--server.port=8501", "--server.enableXsrfProtection=false"]


#docker build -t bayes-front:latest .