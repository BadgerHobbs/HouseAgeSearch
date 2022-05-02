FROM python:3

COPY ./api /app
WORKDIR /app

# Install Python Libraries
RUN pip3 install flask && \
    pip3 install Flask-Cors && \
    pip3 install pydantic
    
ENTRYPOINT ["python3"]
CMD ["api.py"]