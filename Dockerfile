FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install jinja2
EXPOSE 3000
CMD ["python", "main.py"]
