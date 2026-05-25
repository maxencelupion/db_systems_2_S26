FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY prisma ./prisma

RUN prisma generate

COPY . .

CMD ["python", "src/main.py"]
