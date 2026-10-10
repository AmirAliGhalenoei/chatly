FROM python:3.11.15-trixie

LABEL project_name = "Chatly Project"

WORKDIR /src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /src/
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /src/

EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
