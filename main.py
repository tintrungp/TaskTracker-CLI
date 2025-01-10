import shlex
import json
from datetime import datetime

# Default File Name
file_path = 'tasks.json'

'''
Function for saving current data to JSON file.
'''
def writeData(data, nextId):
    # save the next ID for next Task Tracker CLI instance
    data['nextId'] = nextId

    # save data to JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


'''
Function in charge of handling the JSON file opening or
creation if no file exists.
'''
def handleJson():
    # default data for ID creation
    data = {
        'nextId' : 0
    }

    # JSON File Handling
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"\nFile '{file_path}' not found. Creating new file.\n" )
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            data = json.load(file)

    except json.JSONDecodeError:
        print('Error decdoing JSON.')

    return data


'''
Main executing function of Task Tracker CLI. 

Contains all logic and error handling.
'''
def main():
    data = handleJson()
    
    # Task Tracker Logic
    run = True
    while run:
        # gather input
        text = shlex.split(input('task-cli '))

        size = len(text)

        # preprocess for queries that require ID
        if size > 1:
            id = text[1]

        # extract Next ID from last saved data
        if 'nextId' in data:
            nextId = data['nextId']
            del data['nextId']
        
        # gather time of current query
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d-%m-%Y %H:%M")

        ############################
        # Task Add, Update, Delete #
        ############################

        # add new item
        if text[0] == 'add':
            if size == 2:
                data[str(nextId)] = {
                    'description' : text[1],
                    'status' : 'todo',
                    'createdAt' : formatted_time,
                    'updatedAt' : formatted_time,
                }
                
                print('Task added successfully (ID: ', nextId, ')')
                nextId += 1
            
            else:
                print('Please input data to add.')

        # update specified item description and time
        elif text[0] == 'update':
            if size == 3:
                if id not in data:
                    print('Please input existing ID')
                else:
                    data[id]['description'] = text[2]
                    data[id]['updatedAt'] = formatted_time
            

        # delete specified item
        elif text[0] == 'delete':
            if size == 2:
                if id not in data:
                    print('please input existing ID')
                else:
                    del data[id]

        ################
        # Task Marking #
        ################
        
        # change specified item status to in-progress
        elif text[0] == 'mark-in-progress':
            if size == 2:
                if id not in data:
                    print('please input existing ID')
                else:
                    data[id]['status'] = 'in-progress'

        # change specified item status to done
        elif text[0] == 'mark-done':
            if size == 2:
                if id not in data:
                    print('please input existing ID')
                else:
                    data[id]['status'] = 'done'
        
        ################
        # Task Listing #
        ################
        
        elif text[0] == 'list':
            count = 0

            # List all tasks
            if size == 1:
                for id, value in data.items():
                    print(id, ' - ', value['description'])
                    count += 1 

            # List all tasks that are done
            elif text[1] == 'done':
                for id, value in data.items():
                    if value['status'] == 'done':
                        print(id, ' - ', value['description']) 
                        count += 1 

            # List all tasks that are not done
            elif text[1] == 'todo':
                for id, value in data.items():
                    if value['status'] == 'todo':
                        print(id, ' - ', value['description']) 
                        count += 1 

            # List all tasks that are in progress
            elif text[1] == 'in-progress':
                for id, value in data.items():
                    if value['status'] == 'in-progress':
                        print(id, ' - ', value['description']) 
                        count += 1
            if count == 0:
                print('There are no items in the specified list')
                

        #################
        # Exit Handling #
        #################
        if text[0] == 'q' or text[0] == 'quit':
            writeData(data, nextId)
            break

    # Exit Message
    print('\n'
          'Quitting Task Tracker CLI - Have a nice day!'
          '\n')

if __name__ == '__main__':
    main()