FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run", "-p", "5000"]
