FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
WORKDIR /app
COPY ./main.py /app/
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]