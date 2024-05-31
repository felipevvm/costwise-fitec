FROM python:3.12 AS python-build
RUN pip install mysqlclient

FROM python:3.12-slim
COPY --from=python-build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
RUN apt-get update && apt-get install -y libmariadb3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src
COPY config.py config.py

EXPOSE 8080
CMD ["waitress-serve",  "--url-scheme", "https", "--host=0.0.0.0", "--port=8080", "--call", "src:create_app"]
