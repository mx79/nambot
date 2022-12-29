# Use python image
FROM python:3.10

# Args
ARG MONGO_CLUSTER
ENV MONGO_CLUSTER=$MONGO_CLUSTER
ARG REDIS_URL
ENV REDIS_URL=$REDIS_URL
ARG HASH_ALGORITHM
ENV HASH_ALGORITHM=$HASH_ALGORITHM
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

# Use this folder as working directory
WORKDIR /app

# Install requirements
COPY . /app/
RUN pip install -r requirements.txt
RUN pip install frtk-0.1.0.tar.gz

# Run service
CMD gunicorn main:socketio
