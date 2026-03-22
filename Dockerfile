FROM python:latest

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install alembic

COPY . .

ENV PYTHONPATH=/app/app

EXPOSE 8000

CMD sh -c "sleep 5 && alembic upgrade head && (python app/main.py & celery -A app.celery_app:celery_app worker --loglevel=info & celery -A app.celery_app:celery_app beat --loglevel=info)"

# CMD python main.py & alembic upgrade head & celery -A celery_app worker --loglevel=info --beat

# CMD python app/main.py

# CMD sh -c "sleep 5 && alembic upgrade head && (python app/main.py & celery -A app.celery_app:celery_app worker --loglevel=info & celery -A app.celery_app:celery_app beat --loglevel=info)"