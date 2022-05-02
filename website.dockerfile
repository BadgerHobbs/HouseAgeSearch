FROM python:3

COPY ./website /app
WORKDIR /app

# Install Python Libraries
RUN pip3 install flask && \
    pip3 install gunicorn && \
    pip3 install gevent
    
CMD ["gunicorn", "-k", "gevent", "-b", "0.0.0.0:5000", "website:app"]