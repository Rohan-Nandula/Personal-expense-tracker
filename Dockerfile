FROM python:3.8.5
WORKDIR /app
ADD ./app
copy requirements.txt /app
RUN pip install -r requirements.txt
CMD ["python","main.py"]
