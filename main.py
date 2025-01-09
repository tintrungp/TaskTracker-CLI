import shlex
import json
from datetime import datetime

file_path = 'tasks.json'

def writeData(data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    data = {}
    # JSON File Handling
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"\nFile '{file_path}' not found. Creating new file.\n" )
        with open(file_path, 'w') as file:
            json.dump({}, file, indent=4)
            data = json.load(file)

    except json.JSONDecodeError:
        print('Error decdoing JSON.')
    
    # Task Tracker Logic
    run = True
    while run:
        text = shlex.split(input('task-cli '))
        size = len(text)
        idNum = int(list(data.keys())[-1]) + 1
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d-%m-%Y %H:%M")

        ############################
        # Task Add, Update, Delete #
        ############################
        if text[0] == 'add':
            if size == 2:
                data[idNum] = {
                    'description' : text[1],
                    'status' : 'todo',
                    'createdAt' : formatted_time,
                    'updatedAt' : formatted_time,
                }
                
                print('Task added successfully (ID: ', idNum, ')')
                idNum += 1
            
            else:
                print('Please input data to add.')

        elif text[0] == 'update':
            if size == 3:
                id = text[1]
                data[id]['description'] = text[2]
                data[id]['updatedAt'] = formatted_time
            


        elif text[0] == 'delete':
            if size == 2:
                id = text[1]
                del data[id]

        ################
        # Task Marking #
        ################
        elif text[0] == 'mark-in-progress':
            if size == 2:
                id = text[1]
                data[id]['status'] = 'in-progress'

        elif text[0] == 'mark-done':
            if size == 2:
                id = text[1]
                data[id]['status'] = 'done'
        
        ################
        # Task Listing #
        ################
        elif text[0] == 'list':
            # List all tasks
            if size == 1:
                for value in data.values():
                    print(value['description']) 

            # List all tasks that are done
            elif text[1] == 'done':
                for value in data.values():
                    if value['status'] == 'done':
                        print(value['description']) 

            # List all tasks that are not done
            elif text[1] == 'todo':
                for value in data.values():
                    if value['status'] == 'todo':
                        print(value['description']) 

            # List all tasks that are in progress
            elif text[1] == 'in-progress':
                for value in data.values():
                    if value['status'] == 'in-progress':
                        print(value['description']) 

        #################
        # Exit Handling #
        #################
        if text[0] == 'q' or text[0] == 'quit':
            writeData(data)
            break

    # Exit Message
    print('\n'
          'Quitting Task Tracker CLI - Have a nice day!'
          '\n')

if __name__ == '__main__':
    main()
