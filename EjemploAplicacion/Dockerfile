FROM python:3.7.3

#RUN apk add --no-cache python3-dev && pip3 install --upgrade pip
RUN mkdir -p /usr/src/IoT_ImagesWeb

WORKDIR /usr/src/IoT_ImagesWeb
#WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#RUN pip3 install -r requirements.txt

#COPY ["APIObjectDetectionDB.py", "/app"]

EXPOSE 6001

ENTRYPOINT [ "python3" ]

CMD ["app.py"]


