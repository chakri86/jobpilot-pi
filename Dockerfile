FROM node:20-bookworm-slim AS frontend-build

WORKDIR /app/frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend /app/backend
COPY scripts/start-backend.sh /app/scripts/start-backend.sh
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

RUN chmod +x /app/scripts/start-backend.sh \
    && mkdir -p /app/backend/uploads

WORKDIR /app/backend

EXPOSE 5000

CMD ["/app/scripts/start-backend.sh"]
