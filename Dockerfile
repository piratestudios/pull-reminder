FROM python:3.6-stretch
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY src/pull_reminder.py /app/pull_reminder.py

CMD python3 pull_reminder.py