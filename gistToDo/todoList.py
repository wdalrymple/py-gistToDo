class item:

    def __init__(self, description):
        self.description = description
        self.checked = False

    def __format__(self):
        return "- [{}] {}".format( 'x' if self.checked else ' ', self.description)

class itemList:
    def __init__(self, title):
        self.tasks = list()
        self.title = title

    def __format__(self):
        output = "# {}".format(self.title) + "\r"
        for task in self.tasks:
            output.join(task.__format__() + "\r")
        return output


