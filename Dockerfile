
FROM python:3-alpine
WORKDIR /usr/source/app
COPY requirements.txt ./

RUN apk update
RUN echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/main" > /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add gcc
RUN pip install numpy
RUN pip install pandas
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]