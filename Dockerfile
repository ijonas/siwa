FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /usr/src/app/data
EXPOSE 16556
CMD [ "python", "./endpoint.py" ]