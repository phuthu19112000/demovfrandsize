FROM python:3.7.10

COPY . /home/demovfrandsize
# COPY requirements.txt /home
WORKDIR /home/demovfrandsize
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD [ "uvicorn", "main:app" , "--host=0.0.0.0", "--reload" ]

