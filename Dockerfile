FROM python:3.12-slim

LABEL org.opencontainers.image.title="Pixel Boost"
LABEL org.opencontainers.image.description="Pixel Boost API image"

WORKDIR /pixelboost
COPY src/pixelboost/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e .

CMD ["fastapi", "dev", "src/pixelboost/main.py", "--host", "0.0.0.0", "--port", "8000"]