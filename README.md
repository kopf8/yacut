# 📝 [YaCut](https://github.com/kopf8/yacut)

### Contents:

1. [Project tech stack](#project-tech-stack)
2. [Description](#project-description)
3. [Project deployment](#project-deployment)
4. [Sample API requests](#sample-api-requests)
5. [Project created by](#project-created-by)
<br><hr>

## Project tech stack:
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
- ![SQLAlchemy](https://img.shields.io/badge/SQLALCHEMY-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white&logoSize=auto)

<br><hr>
## Project description:
The YaCut project is a link shortening service. Its purpose is to associate a long user link with a short one, 
which is offered by the user himself or provided by the service.

## Project deployment:
## Установка и запуск проекта

### Запуск проекта:
Fork this repository into your GitHub profile.
Then clone your repository to your local machine via SSH:
```bash
git clone git@github.com:your_github_username/your_repository_name.git
```
Then switch to project directory:
```bash
cd yacut
```
Then create & activate a virtual environment, upgrade pip and install project requirements:
```bash
python -m venv .venv
source .venv/Scripts/activate #for Windows users
source .venv/bin/activate #for Linux users
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Create .env file in project directory: 
```bash
touch .env
```
This file must contain the following data: 
```
FLASK_APP
FLASK_DEBUG
DATABASE_URI
SECRET_KEY
```
Hint - There's a sample file _**.env.example**_ which can be used as a draft.

Create & update database by performing the following steps:
1. Make sure you have your virtual environment actiated, and run interactive Flask shell by the following command:
```bash
flask shell
```
2. Input the following commands:
```bash
>>> from yacut import db
>>> db.create_all()
```
3. Make sure a new file _**db.sqlite3**_ has appeared in the project directory:
4. Exit from the interactive Flask shell:
```bash
>>> exit()
```
5. Create migrations scenarios repository:
```bash
flask db init
```
6. Run migrations:
```bash
flask db migrate
flask db upgrade
```

Then run project in development mode:
```bash
flask run
```
Project will be available at http://127.0.0.1:5000/

## Sample API requests
All requests were done & can be checked in [Postman](https://www.postman.com/)

http://127.0.0.1:5000/api/id/ — POST-request to create a new short link

Request:
```
{
  "url": "string",
  "custom_id": "string"
}
```
Response:
```
{
  "url": "string",
  "short_link": "string"
}
```
[http://127.0.0.1:5000/api/id/<short_id>/](http://127.0.0.1:5000/api/id/<short_id>/) — GET-request to get the original link saved for given short link.

Response:
```
{
  "url": "string"
}
```

## Project created by:
### [✍️ Maria Kirsanova](https://github.com/kopf8)