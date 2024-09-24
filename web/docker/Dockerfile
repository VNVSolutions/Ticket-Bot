FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /TicketBot

WORKDIR /TicketBot

COPY web/requirements.txt /TicketBot/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /TicketBot/

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "TicketBot.wsgi:application"]
