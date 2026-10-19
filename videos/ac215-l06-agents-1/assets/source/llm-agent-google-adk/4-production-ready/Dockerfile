FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .env.example ./
RUN uv pip install --system google-adk fastapi uvicorn python-dotenv

COPY app/ ./app/

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
