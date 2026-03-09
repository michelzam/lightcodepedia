FROM python:3.10-slim

WORKDIR /app

COPY _requirements.runtime.txt .
RUN pip install --no-cache-dir -r _requirements.runtime.txt

COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
