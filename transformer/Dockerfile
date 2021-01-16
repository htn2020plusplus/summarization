FROM pytorch/pytorch:latest

# Copy deps
COPY requirements.txt /

# Install any dependencies
RUN pip install -r /requirements.txt

# Copy your Python file to the image
COPY *.py /

# pre-download
RUN python /pre_warm.py

# Tell Docker how to start your script
ENTRYPOINT [ "python", "/app.py" ]