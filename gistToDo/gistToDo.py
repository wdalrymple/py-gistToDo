import click
import cmd
from gistToDo.todoList import TaskList


class REPL(cmd.Cmd):
    def __init__(self, ctx):
        cmd.Cmd.__init__(self)
        self.ctx = ctx

    def default(self, line):
        subcommand = cli.commands.get(line)
        if subcommand:
            self.ctx.invoke(subcommand)
        else:
            return cmd.Cmd.default(self, line)

class toDoConfig:

    def __init__(self):
        self.task_lists = []
        self.current_task_list = None
        self.user_id = ''
        self.password = ''

pass_toDo = click.make_pass_decorator(toDoConfig, ensure=True)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    gist-to-do is a CLI for managing a To-Do list backed against a users github Gist's
    """
    """defines the context object used through CLI"""
    if ctx.invoked_subcommand is None:
        ctx.obj = toDoConfig()
        repl = REPL(ctx)
        repl.cmdloop()


@cli.command()
@click.option('--user_id', prompt='User Id', help='Github user id')
@click.option('--password', prompt='Password', help='Github password')
@pass_toDo
def login(toDo, user_id, password):
    """Login with your github credentials (userid/password). These are cached locally."""
    click.echo('login')
    toDo.user_id = user_id
    toDo.password = password

@cli.command()
@pass_toDo
def whoami(toDo):
    """Ouput the userid of the currently logged in user"""
    click.echo('User: ' + toDo.user_id)


@cli.command()
@pass_toDo
def list(toDo):
    """List known gists that follow the pattern gistToDo-{title}.md"""
    click.echo('stuff...')


@cli.command()
@click.pass_context
def show(toDo):
    """Display the current ToDo list loaded"""
    print(toDo.obj.current_task_list.__format__())

    if toDo is None or toDo.current_task_list is None:
        print('Please load a list first.')
    else:
        print(toDo.current_task_list.__format__())


@cli.command()
@click.option('--name', prompt='List Name', help='The name of the task list to create.')
@pass_toDo
def create(toDo, name):
    """Create a new ToDo List"""
    new_task_list = TaskList(name)
    toDo.task_lists.append(new_task_list)
    toDo.current_task_list = new_task_list
    print('Created new list "{}"'.format(name))


@cli.command()
@click.option('--task', prompt='Task', help='The description of the task that you want to create.')
@pass_toDo
def add(toDo, task):
    """Add a new task"""
    if toDo is None or toDo.current_task_list is None:
        print('Please create or load a list first.')
    else:
        new_task = toDo.current_task_list.add(task)
        print(new_task.__format__('Added: '))


@cli.command()
def check():
    """Check/Uncheck tasks in the current list"""
    click.echo('check')


@cli.command()
@click.option('--id', prompt='List Id', help='The id of the list that you want to load.')
@click.pass_context
def load(toDo, id):
    """Load and set a ToDo list from known gists that follow the pattern gistToDo-{title}.md"""
    l = TaskList('')
    gist = "# Here I go again\n-[x] poop\n-[ ] dog shit"
    l.load_gist(gist)

    l.tasks[1].checked=True

    toDo.obj.current_task_list = l
    print(toDo.obj.current_task_list.__format__())
    print('Successfully loaded list')


@cli.command()
@click.option('--task', prompt='Task', help='The task number that you want to delete.')
@pass_toDo
def delete(toDo, task):
    """Delete a task."""
    if toDo is None or toDo.current_task_list is None:
        print('Please load a list first.')
    else:
        if toDo.current_task_list.tasks.length > 0 and task < toDo.current_task_list.tasks.length:
            print('Deleted task: ' + toDo.current_task_list.tasks[task].description)
            toDo.current_task_list.delete(task)
        else:
            print('There is no task number {} in the list.'.format(task))


@cli.command()
@pass_toDo
def config(toDo):
    """Configure options for cli."""
    click.echo('config')


@cli.command()
@pass_toDo
def archive(toDo):
    """archive all checked tasks"""
    if toDo is None or toDo.current_task_list is None:
        print('Please load a list first.')
    else:
        if toDo.current_task_list.tasks.length > 0:
            print('Archived tasks')
            toDo.current_task_list.archive()
        else:
            print('There are no tasks to archive')

if __name__ == "__main__":
    print('run man')
    cli()