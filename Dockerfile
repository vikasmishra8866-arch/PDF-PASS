# Use official base Python image
FROM python:3.10-slim

# Prevent Python from writing .pyc files & enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Linux system C++ dependencies, qpdf, and pdfcrack
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    qpdf \
    libqpdf-dev \
    pdfcrack \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . /app/

# Expose Streamlit default port
EXPOSE 8501

# Health check setup
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch Streamlit with external binding
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
