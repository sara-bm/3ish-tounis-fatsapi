FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app
COPY ./main.py /app/
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt