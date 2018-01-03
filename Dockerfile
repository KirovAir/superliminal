# Use an official Python runtime as a parent image
FROM diaoulael/subliminal
LABEL maintainer=KirovAir

# Set the working directory to /app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
ADD . /usr/src/app

# Add Flask
RUN pip install Flask

# Make port 8978 available to the world outside this container
EXPOSE 8978

# Remove subliminal ENTRYPOINT 
ENTRYPOINT []

# Run app.py when the container launches
CMD ["python", "/usr/src/app/app.py", "-p 8978"]
