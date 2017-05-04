class TaskItem:

    def __init__(self, description):
        self.description = description
        self.checked = False

    def __format__(self, index):
        return "{} [{}] {}".format('-' if index is None else str(index) + ".", 'x' if self.checked else ' ', self.description)


class TaskList:

    def __init__(self, title):
        self.tasks = list()
        self.title = title

    def load_gist(self, gist):
        self.type = type
        lines = gist.splitlines()
        self.title = lines[0].replace('#','')
        lines.remove(lines[0])
        for line in lines:
            task = TaskItem(line.split('] ')[1])
            task.checked = True if line.count("[x]") > 0 else False
            self.tasks.append(task)

    def add(self, task_description):
        new_task = TaskItem(task_description)
        self.tasks.append(new_task)
        return new_task

    def delete_all_tasks(self):
        self.tasks.clear()

    def delete(self, index):
        self.tasks.remove(self.tasks[index])

    def check(self, index, **kwargs):
        if 'checked' in kwargs:
            self.tasks[index].checked = bool(kwargs['checked'])
        else:
            self.tasks[index].checked = not self.tasks[index].checked

    def archive(self):
        for line in self.tasks:
            if line.checked:
                self.tasks.remove(line)

    def __format__(self):
        return "# {}".format(self.title) + "\n" + "\n".join(task.__format__(index) for index, task in enumerate(self.tasks, 1))


