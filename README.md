# Travel Project
1. Build docker containers:
`docker-compose build` 
2. Start docker containers:
`docker-compose up -d`
3. In app_container load migrations:
`alembic upgrade head`


## For .env listed below variables need to be added:

Your web application port `APP_PORT`

Your web application host `APP_HOST`

Your web application reload preference `APP_RELOAD`

Your web application origins `APP_ORIGINS`

Your database user `APP_DB_USER`

Your database password `APP_DB_PASSWORD`

Your database host `APP_DB_HOST`

Your database port `5432`

Your database  name `APP_DB_NAME`

Your JWT secret, that will be used for creating JWT tokens `APP_JWT_SECRET`

Your JWT encoding algorithm `APP_JWT_ALGORITHM`

## Project documentation is structured by FastApi itself and can be accesible with

### `http://<APP_HOST>:<APP_HOST>/docs/`

<img width="1805" height="899" alt="image" src="https://github.com/user-attachments/assets/e7d430ca-1085-4a90-80cc-3a287e85423e" />

### `http://<APP_HOST>:<APP_HOST>/redoc/`

<img width="1918" height="984" alt="image" src="https://github.com/user-attachments/assets/6440d52c-d17f-4e2e-a958-e317ca2a6719" />

I also added json file
`"app\utils\openapi.json"`
alembic.ini is not in .gitignore for demonstration purposes
