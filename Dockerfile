FROM python:3.12.11-trixie

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y make

CMD ["bash"]