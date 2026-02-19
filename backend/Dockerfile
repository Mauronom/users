
FROM python:3.9

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /code/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /code/

#CMD ["sleep", "infinity"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]