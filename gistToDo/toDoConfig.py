import os
from gistToDo.todoList import TaskList


class MarkDownFile:
    def __init__(self, file_name, type, location, task_list):
        self.type= type
        self.location= location
        self.file_name= file_name
        self.task_list = task_list


class ToDoConfig:
    def __init__(self):
        self.task_lists = []
        self.current_task_list = None
        self.user_id = ''
        self.password = ''
        self.enableLocal = False
        self.enableGist = True
        self.github_url = 'http://github.com'
        self.local_storage = None

    def load_local_storage_lists(self):
        #file object = open('123.txt', 'w+')
        #object.write(self.current_task_list.__format__())
        if self.local_storage is not None: os.chdir(self.local_storage)
        for gist in os.listdir():
            if gist.endswith('.md'):
                gist_file = open(gist)
                new_task_list = TaskList('')
                new_task_list.load_gist(gist_file.read())
                new_list_item = MarkDownFile(gist, 'LOCAL', os.pardir + '\\' + gist, new_task_list)
                self.task_lists.append(new_list_item)
        return self.task_lists