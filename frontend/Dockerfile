FROM registry.access.redhat.com/ubi9/python-311:latest

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD app.py .

EXPOSE 8080

CMD ["python", "app.py"]
