FROM python:3.10
WORKDIR /usr/src/app
COPY . .


#install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# start server
CMD ["python", "./server.py"]
