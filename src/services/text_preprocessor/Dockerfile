FROM python:3.8-slim AS builder 

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.8-slim

RUN apt-get update

COPY --from=builder /opt/venv /opt/venv 

WORKDIR /home/text_preprocessor/

COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["python", "main.py"]

# Uncomment for debug mode
# CMD ["-d"]
