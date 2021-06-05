FROM python:3.5.5-alpine
WORKDIR /app
ADD ./app
copy requirements.txt /app
RUN pip install -r requirements.txt
CMD ["python","main.py"]
