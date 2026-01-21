FROM python:3.11

# Install Git if needed
RUN apt-get update && apt-get install -y git

EXPOSE 8080
WORKDIR /app

COPY . ./

RUN pip install --upgrade -r requirements.txt

# Pre-download the HuggingFace model
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

CMD ["python", "app.py"]