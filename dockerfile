# Use Python 3.9 as the base image
FROM python:3.10-slim

# Set environment variables to reduce Docker image size and improve performance
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /notebooks

# Copy the requirements file and install dependencies
COPY requirements.txt /notebooks/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY notebooks /notebooks/

# Expose ports if needed (e.g., for Jupyter Notebook or other services)
EXPOSE 8888

# Default command for the container
# You can modify this to run a specific Python script or Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]