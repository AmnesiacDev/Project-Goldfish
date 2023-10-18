FROM python:3.9.7

WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Install the application dependencies
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]
