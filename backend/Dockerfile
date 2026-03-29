
FROM python:3.9

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && apt-get clean \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g @anthropic-ai/claude-code

COPY requirements.txt /code/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /code/

#CMD ["sleep", "infinity"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]