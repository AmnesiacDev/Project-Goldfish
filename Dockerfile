FROM python:3.9.7

# Set the working directory in the container

# Install the application dependencies
RUN pip install -r requirements.txt

EXPOSE 8000

CMD "python main.py"
