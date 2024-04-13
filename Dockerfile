FROM python:3.12-alpine 
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && pip install "poetry==1.8.0" && poetry config virtualenvs.create false && poetry install --no-cache
COPY . .
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]