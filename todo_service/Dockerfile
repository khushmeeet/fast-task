FROM python:3.12.0a5-bullseye
RUN apt-get update && apt-get -y upgrade
COPY ./app /root/home/app
WORKDIR /root/home/app
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "main:app"]