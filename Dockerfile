FROM python:3.13-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
COPY smart_ai_agent/requirements.txt /code/
RUN pip install --upgrade pip setuptools wheel
RUN apt-get update && apt-get install -y python3.13-dev libpq-dev build-essential
RUN pip install -r requirements.txt
# Copy project
COPY . /code/