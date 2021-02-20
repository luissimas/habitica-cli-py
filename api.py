import json
import re

import requests
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import config

apiHeader = {
    'x-client': f'{config.creatorId}-{config.appName}',
    'x-api-user': config.userId,
    'x-api-key': config.apiKey
}


def testAPI():
    url = 'https://habitica.com/api/v3/status'

    session = Session()

    parameters = {
        'teste': 'teste'
    }

    try:
        response = session.get(url, headers=apiHeader, params=parameters)
        data = json.loads(response.text)

        print(json.dumps(data, indent=4, sort_keys=True))

    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

def login(username, password):
    url = 'https://habitica.com/api/v3/user/auth/local/login'

    session = Session()

    parameters = {
        'username': username,
        'password': password
    }

    try:
        response = session.post(url, headers=apiHeader, data=parameters)
        data = json.loads(response.text)

        print(json.dumps(data, indent=4, sort_keys=True))

    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

def newTask(taskText, taskType, taskNotes, taskDifficulty):
    url = 'https://habitica.com/api/v3/tasks/user'

    session = Session()

    aliasText = taskType + '-' + taskText.lower().strip().replace(' ', '-')

    parameters = {
        'text': '# ' + taskText,
        'type': taskType,
        'alias': aliasText,
        'notes': taskNotes,
        'priority': taskDifficulty
    }

    try:
        response = session.post(url, headers=apiHeader, data=parameters)
        data = json.loads(response.text)

        #print(json.dumps(data['data'], indent=4, sort_keys=True))

        return data['data']['_id']

    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

def deleteTask(taskId):
    url = f'https://habitica.com/api/v3/tasks/{taskId}'

    session = Session()

    try:
        response = session.delete(url, headers=apiHeader)
        data = json.loads(response.text)

        #print(json.dumps(data, indent=4, sort_keys=True))

    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

def addChecklist(taskId, taskText):
    url = f'https://habitica.com/api/v3/tasks/{taskId}/checklist'

    session = Session()

    parameters = {
        'text': taskText,
    }

    try:
        response = session.post(url, headers=apiHeader, data=parameters)
        data = json.loads(response.text)

        #print(json.dumps(data['data'], indent=4, sort_keys=True))

    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

def listTasks():
    url = 'https://habitica.com/api/v3/tasks/user'

    session = Session()

    try:
        response = session.get(url, headers=apiHeader)
        data = json.loads(response.text)

        #print(json.dumps(data['data'], indent=4, sort_keys=True))

        return data['data']


    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

def checkTask(taskId, check):
    url = f'https://habitica.com/api/v3/tasks/{taskId}/score/{"up" if check else "down"}'

    session = Session()

    try:
        response = session.post(url, headers=apiHeader)
        data = json.loads(response.text)

        #print(json.dumps(data, indent=4, sort_keys=True))

    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)


def checkChecklist(taskId, itemId):
    url = f'https://habitica.com/api/v3/tasks/{taskId}/checklist/{itemId}/score'

    session = Session()

    try:
        response = session.post(url, headers=apiHeader)
        data = json.loads(response.text)

        #print(json.dumps(data, indent=4, sort_keys=True))

    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)
