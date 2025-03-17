FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
