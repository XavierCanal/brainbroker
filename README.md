# brainbroker

## Requirements local development

- python 3.6
- pipenv
- docker (mongoDB)

## Setup

- clone the repositoryç
- cd into the repository
- Create docker container for mongoDB with 
  - `docker run -d -p 27017:27017 --name brainbroker-mongo mongo`
- Install dependencies with `pipenv install`
- Run the application with `pipenv run python app.py` or using pycharm or any other IDE that supports pipenv