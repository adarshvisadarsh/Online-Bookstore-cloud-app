# FROM python:3
# USER root
# WORKDIR /app
# ADD . /app
# RUN pip install  -r requirements.txt
# CMD [ "python", "./user_service.py" ]


FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /catalogue
WORKDIR /catalogue
COPY requirements.txt /catalogue/
RUN pip install -r requirements.txt
COPY . /catalogue/