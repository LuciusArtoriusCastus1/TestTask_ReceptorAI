FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r req.txt

EXPOSE 8000

CMD ["sh", "-c", "cd app && uvicorn main:app --host 0.0.0.0 --port 8000"]
