FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD python wait_for_db.py && python app.py
