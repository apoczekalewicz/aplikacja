FROM registry.access.redhat.com/ubi9/python-311:latest

# BUG: using ADD instead of COPY (ACS: "ADD Command used instead of COPY")
ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    # BUG: installing curl and wget (ACS: "Curl in Image", "Wget in Image")
    dnf install -y curl wget && \
    dnf clean all

# BUG: installing openssh-server exposes SSH port (ACS: "Secure Shell Port Exposed")
RUN dnf install -y openssh-server && dnf clean all
EXPOSE 22

ADD app.py .

EXPOSE 8080

CMD ["python", "app.py"]
