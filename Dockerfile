FROM python:latest

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install alembic

COPY . .

ENV PYTHONPATH=/app/app

EXPOSE 8000

CMD sh -c "sleep 5 && alembic upgrade head && (python app/main.py & celery -A celery -A app.celery_app:celery_app worker --loglevel=info -P solo & celery -A app.celery_app:celery_app beat --loglevel=info)"
