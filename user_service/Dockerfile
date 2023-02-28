FROM python:3.12.0a5-bullseye
RUN apt-get update && apt-get -y upgrade
ARG MONGO_URI
ARG SECRET_KEY
ENV MONGO_URI $MONGO_URI
ENV SECRET_KEY $SECRET_KEY
COPY ./app ~/app
WORKDIR ~/app
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "main:app"]