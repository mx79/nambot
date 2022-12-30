# Use python image
FROM python:3.10

# Use this folder as working directory
WORKDIR /app

# COpy all and install requirements
COPY . /app/
RUN pip install -r requirements.txt
RUN pip install frtk-0.1.0.tar.gz

# Run service
CMD ["python", "app.py"]
