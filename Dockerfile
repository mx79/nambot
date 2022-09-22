# Use python image
FROM python

# Use this folder as working directory
WORKDIR /app

# Ports
EXPOSE 5000

# Install requirements
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy actions folder to working directory
COPY . /app/

# Run service
CMD ["bash", "./launch.sh"]
