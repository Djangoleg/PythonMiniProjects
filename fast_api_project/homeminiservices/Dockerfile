FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /usr/local/homeminiservices
RUN pip3 install --upgrade pip
COPY ./ /usr/local/homeminiservices
RUN pip3 install -r /usr/local/homeminiservices/requirements.txt
