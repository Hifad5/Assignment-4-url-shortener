#This will use the offical runtime as python image
FROM python:3.9-slim

# This will configure the directoy in the container
WORKDIR /app

# This will copy the coniner in the directory contents
COPY . /app

# This will install any python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# This will make port 5000 aviablble outside of the container
EXPOSE 5000

# These are the commands to run the application
CMD ["python", "app.py"]
