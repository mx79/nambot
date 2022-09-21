# Use python image
FROM python

# Use this folder as working directory
WORKDIR /app

# Install requirements
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy actions folder to working directory
COPY data /app/data
COPY pkg/bot/models /app/models
COPY pkg /app/pkg
COPY worker.py /app/

# Run worker file inside the container
CMD ["python", "./main.py"]