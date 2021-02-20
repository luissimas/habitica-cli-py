import argparse
from getpass import getpass
import sys
import re

import api


def listTasks(tasksArray, showIndex):
    tasksArray.sort(key=lambda task: task['type'])

    print('\n------ Daily ------')
    if showIndex:
        for task in tasksArray:
            if tasksArray.index(task) >= 1:
                if tasksArray[tasksArray.index(task)]['type'] == 'habit' and tasksArray[tasksArray.index(task) - 1]['type'] != 'habit':
                    print('-------------------')
                    print('\n------ Habit ------')
                elif (tasksArray[tasksArray.index(task)]['type'] == 'todo' and tasksArray[tasksArray.index(task) - 1]['type'] != 'todo'):
                    print('-------------------')
                    print('\n------ Todo ------')

            print(f'[{tasksArray.index(task)}] ' + re.sub(r'\#.', '', task['text']) + '\n' + task['notes'])

            if (task['type'] != 'habit') and (len(task['checklist'])):
                for item in task['checklist']:
                    print('     ', f'[{tasksArray.index(task)}.{task["checklist"].index(item)}]', '[X]' if item['completed'] else '[ ]', item['text'])
        print('-------------------')
    else:
        for task in tasksArray:
            if tasksArray.index(task) >= 1:
                if tasksArray[tasksArray.index(task)]['type'] == 'habit' and tasksArray[tasksArray.index(task) - 1]['type'] == 'daily':
                    print('\n------ Habit ------')
                elif tasksArray[tasksArray.index(task)]['type'] == 'todo' and tasksArray[tasksArray.index(task) - 1]['type'] == 'habit':
                    print('\n------ Todo ------')

            print(f'[{tasksArray.index(task)}] ' + re.sub(r'\#.', '', task['text']) + '\n' + task['notes'])

        print('-------------------')

    return tasksArray



arg = argparse.ArgumentParser(description='A CLI interface for Habitica')

arg.add_argument('--test', '-t', action='store_true', help='Test the state of the API')
arg.add_argument('--list', '-l', action='store_true', help='List all the tasks')
arg.add_argument('--delete', '-d', action='store_true', help='Delete a task')
arg.add_argument('--newtask', '-nt', action='store_true', help='Add a new task')
arg.add_argument('--check', '-ck', action='store_true', help='Check a task')

parser = arg.parse_args()


if len(sys.argv) <= 1:
    arg.print_help()
else:
    if parser.test:
        api.testAPI()
    if parser.newtask:
        createdId = api.newTask(input('Título: '), input('Tipo: '), input('Descrição: '), input('Dificuldade (0.1 - 1 - 1.5 - 2): '))

        checklistOption = input('Adicionar checklist? [y/N] ')

        while checklistOption== 'y':
            api.addChecklist(createdId, input('Descrição: '))

            checklistOption = input('Continuar adicionando itens na checklist? [y/N] ')
    if parser.delete:
        tasksArray = api.listTasks()
        listTasks(tasksArray, True)

        api.deleteTask(tasksArray[int(input('Task index: '))]['_id'])
    if parser.check:
        tasksArray = api.listTasks()
        listTasks(tasksArray, True)

        indexString = input('Index: ')

        if '.' in indexString:
            api.checkChecklist(tasksArray[int(indexString[0])]['_id'], tasksArray[int(indexString[0])]['checklist'][int(indexString[2])]['id'])
        else:
            api.checkTask(tasksArray[int(indexString[0])]['_id'], True)
    if parser.list:
        listTasks(api.listTasks(), True)



