FROM python:3.9.0

WORKDIR /home/

RUN  echo "$PRIVATE_SSH_KEY" > id_ed25519.pub
RUN  git clone git@github.com:1992JYP-ASC/ASC_livingparadise.git


WORKDIR /home/ASC_livingparadise


RUN pip install -r Requirements.txt

RUN pip install pipenv
RUN pipenv install --dev
RUN pipenv run python manage.py makemigrations
RUN pipenv run python manage.py migrate



EXPOSE 8000

CMD ["pipenv","run","python","manage.py","runserver","0.0.0.0:8000"]
