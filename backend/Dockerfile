FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

ENTRYPOINT [ "uvicorn" ]

CMD ["main:app", "--host", "0.0.0.0", "--port", "8000"]