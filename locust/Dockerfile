FROM python:3.9

WORKDIR /workspace

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

COPY . /workspace/locust

CMD ["locust", "-f", "locust/stress_test.py", "--host=http://0.0.0.0:8000"]



