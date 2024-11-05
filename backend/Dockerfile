FROM python:3.11.6
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY whine_meter whine_meter
CMD ["python", "-m", "whine_meter"]
