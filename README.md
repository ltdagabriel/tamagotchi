Setup
------

Install requirements

    pip install -r requirements.txt

ADD FLASK_APP

    set FLASK_APP=init.py
    set FLASK_ENV=development

RUN

    Python -m flask run --host=0.0.0.0 --port=80