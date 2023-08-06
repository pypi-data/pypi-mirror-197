from ubuntu:20.04 as build 
WORKDIR /app
RUN apt update 
RUN apt install python3.8 -y 
RUN apt install pip  -y
RUN pip3 install sphinx==5.3.0
RUN apt install git -y
RUN git clone -b dev http://auth2:glpat-THSizjsdQQuivV5YCwiW@10.217.50.40:8190/industry4/nazca-4.0/spark-ml/python-sdk.git
WORKDIR /app/python-sdk
RUN pip install -r requirements.txt
RUN sphinx-apidoc -f -o docs/source nazca4sdk nazca4sdk\datahandling\hotstorage\model\user_variable.py
RUN sphinx-build -b html docs/source docs/build/html


from nginx:latest
COPY --from=build /app/python-sdk/docs/build/html/ /usr/share/nginx/html/
