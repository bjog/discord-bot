FROM python:3.7-stretch

RUN apt-get update -y

RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python","bot.py"]