FROM python:3.8-slim
#RUN apt-get update
#RUN apt-get install -y python3-pip
COPY . /Module4_VehicleTracking
WORKDIR /Module4_VehicleTracking
RUN pip install -r requirements.txt
CMD ["python", "./tracker/__main__.py"]