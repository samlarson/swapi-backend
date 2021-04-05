FROM python:3.8.9-alpine3.13

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app
ENV PATH="/app:${PATH}"
EXPOSE 8080

ENTRYPOINT ["./run.sh"]
