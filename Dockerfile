FROM python:3.6-stretch
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY src/slack_pull_reminder.py /app/slack_pull_reminder.py

CMD python3 slack_pull_reminder.py