FROM python:3.11.6

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "mahabharata_chatbot.py"]