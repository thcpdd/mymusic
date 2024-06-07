FROM python:3.10
LABEL "author"="Rainbow"
COPY . /web/MyMusic
WORKDIR /web/MyMusic
RUN pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["uwsgi", "--ini", "uwsgi.ini"]
