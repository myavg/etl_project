FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["bash", "-lc", "python src/wait_for_db.py && python main.py"]
