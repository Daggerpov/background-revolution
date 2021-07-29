FROM python:3.9.6

ADD main.py . 

RUN pip install pillow 

CMD ["python", "./main.py"] 

