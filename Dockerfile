# Set the baseImage to use for subsequent instructions. FROM must be the first instruction in a Dockerfile.
# FROM baseImage
# FROM baseImage:tag
# FROM baseImage@digest
FROM python:3.8-slim-buster

# Set the working directory
# WORKDIR /the/workdir/path
WORKDIR /app

# Set the environment variable key to the value.
ENV PORT 8080

# Copy files or folders from source to the dest path in the image's filesystem.
COPY requirements.txt requirements.txt

# Execute any commands on top of the current image as a new layer and commit the results.
RUN pip3 install -r requirements.txt

COPY . .

# Provide defaults for an executing container.
CMD [ "python3", "main.py" ]