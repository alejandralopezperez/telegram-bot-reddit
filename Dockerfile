FROM python:3.7-alpine

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev

WORKDIR /app/learning_path

COPY . /app/learning_path

ENV PYTHONPATH "${PYTHONPATH}:/app/learning_path"

RUN pip install -r requirements.txt

VOLUME ["/newsbot/data"]

CMD ["python", "newsbot/main.py"]
