FROM python:alpine3.12
RUN pip install --no-cache-dir pyowm

ADD getweather.py /
CMD [ "python", "./getweather.py" ]