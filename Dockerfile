FROM python:3.7-slim
#RUN apk update && apk add python3-dev \
#                        gcc \
#                        libc-dev \
#                        uwsgi-python3
RUN apt-get update
RUN apt-get install -y gcc weasyprint
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PYTHONPATH /usr/local/lib/python3.7/site-packages:/usr/lib/python3.6/site-packages
CMD ["uwsgi", "--ini", "app.ini"]
