FROM python:3.9

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./src /workspace/src

CMD ["fastapi", "run", "src/app.py", "--port", "8000"]



