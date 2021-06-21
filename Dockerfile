# pull official base image
FROM python:3.9
RUN apt-get update

# set work directory
WORKDIR /code

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get install wkhtmltopdf -y


# copy project
ADD . .
EXPOSE 5055