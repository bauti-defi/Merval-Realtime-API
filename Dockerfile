FROM python:3.8-slim

WORKDIR /usr/app/merval/server/

RUN pip install fastapi uvicorn pyhomebroker 

COPY . .

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]