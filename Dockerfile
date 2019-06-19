FROM python:3.5

COPY ./ ./

RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]