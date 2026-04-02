FROM python:3.11-slim

# Env variable for uv and python
ENV PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# System dependencies forvLLM
RUN apt-get update && apt-get install -y \
    curl git build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY requirements.txt .

RUN uv pip install -r requirements.txt

COPY src/ /app/src/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]