FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
<<<<<<< HEAD
CMD ["uvicorn", "exp4:app", "--host", "0.0.0.0", "--port", "8000"]
=======
CMD ["uvicorn", "exp4:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 1393b42165e9824f1f45aeccb04286db281b8858
