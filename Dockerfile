FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/Cheemeng97/Group9_IRProject.git

CMD [ "python3", "./startSpider.py" ]