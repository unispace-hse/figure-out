# Pull base image
FROM python:3.11.5-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install PostgreSQL client
RUN apt-get update && \
    apt-get install -y postgresql-client


# Set work directory
WORKDIR /code

# Install dependencies
COPY ./docker/requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web.wsgi:application"]