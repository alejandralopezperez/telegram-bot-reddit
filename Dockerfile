FROM python:3.9-alpine

WORKDIR /app/learning_path

COPY . /app/learning_path

ENV PYTHONPATH "${PYTHONPATH}:/app/learning_path"

RUN pip install -r requirements.txt

CMD ["python", "newsbot/main.py"]
