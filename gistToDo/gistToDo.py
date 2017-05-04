import click
import os
from click_shell import shell
from gistToDo.todoList import TaskList
from gistToDo.toDoConfig import ToDoConfig


@shell(prompt='gistToDo > ', intro='Initialzing gist-to-do...')
@click.pass_context
def cli(ctx):
    """
    gist-to-do is a CLI for managing a To-Do list backed against a users github Gist's
    """
    """defines the context object used through CLI"""
    ctx.obj = ToDoConfig()


@cli.command()
@click.option('--user_id', prompt='User Id', help='Github user id')
@click.option('--password', prompt='Password', hide_input=True, help='Github password')
@click.pass_obj
def login(toDo, user_id, password):
    """Login with your github credentials (userid/password). These are cached locally."""
    toDo.user_id = user_id
    toDo.password = password

@cli.command()
@click.pass_obj
def whoami(toDo):
    """Ouput the userid of the currently logged in user"""
    click.echo('User: ' + toDo.user_id)


@cli.command()
@click.pass_obj
def list(toDo):
    """List known gists that follow the pattern gistToDo-{title}.md"""
    toDo.load_local_storage_lists()
    for i in range(0, toDo.task_lists.__len__()):
        click.echo("{0}. {1} [{2}]".format(i+1, toDo.task_lists[i].task_list.title, toDo.task_lists[i].type))


@cli.command()
@click.pass_obj
def show(toDo):
    """Display the current ToDo list loaded"""
    if toDo is None or toDo.current_task_list is None:
        click.UsageError('Please load a list first.')
    else:
        click.echo(toDo.current_task_list.__format__())


@cli.command()
@click.option('--name', prompt='List Name', help='The name of the task list to create.')
@click.pass_obj
def create(toDo, name):
    """Create a new ToDo List"""
    new_task_list = TaskList(name)
    toDo.task_lists.append(new_task_list)
    toDo.current_task_list = new_task_list
    click.echo('Created new list "{}"'.format(name))


@cli.command()
@click.option('--task', prompt='Task', help='The description of the task that you want to create.')
@click.pass_obj
def add(toDo, task):
    """Add a new task"""
    if toDo is None or toDo.current_task_list is None:
        click.UsageError('Please create or load a list first.')
    else:
        new_task = toDo.current_task_list.add(task)
        click.echo(new_task.__format__('Added..'))


@cli.command()
@click.option('--all', is_flag=True, help='Show both checked and un-checked tasks')
@click.option('--task', help='Mark an task as checked by id in the list.')
@click.pass_obj
def check(toDo, all, task):
    """Check un checked tasks in the current list. If no task id is provided, the user is prompted for each list item.
    An 'x' will check an item, a ' ' or a 'u' will uncheck it.
    Use the --all option to show all list items and allows the user to ucheck an item."""
    if task is not None and task != '':
        if toDo.current_task_list.tasks.__len__() > 0 and int(task) < toDo.current_task_list.tasks.__len__():
            click.echo('Checked task: {}'.format(toDo.current_task_list.tasks[int(task)-1].description))
            toDo.current_task_list.check(int(task)-1)
        else:
            click.BadParameter('There is no task number {} in the list.'.format(task))
    else:
        for i in range(0, toDo.current_task_list.tasks.__len__()):
            if toDo.current_task_list.tasks[i].checked == False or all:
                res = click.prompt(toDo.current_task_list.tasks[i].__format__(i+1) + '? Default', 'x' if toDo.current_task_list.tasks[i].checked == False else ' ')
                if res == ' ' or res == 'x' or res == 'u':
                    toDo.current_task_list.check(i, checked=True if res == 'x' else False)


@cli.command()
@click.option('--id', prompt='List Id', help='The id of the list that you want to load.')
@click.pass_context
def load(toDo, id):
    """Load and set a ToDo list from known gists that follow the pattern gistToDo-{title}.md"""
    l = TaskList('')
    gist = "# Here I go again\n-[x] item 1\n-[ ] item 2"
    l.load_gist(gist)

    l.tasks[1].checked=True

    toDo.obj.current_task_list = l
    toDo.obj.task_lists.append(toDo.obj.current_task_list)
    print(toDo.obj.current_task_list.__format__())
    print('Successfully loaded list')


@cli.command()
@click.option('--task', prompt='Task', help='The task number that you want to delete.')
@click.option('--all', is_flag=True, help='Delete all tasks')
@click.pass_obj
def delete(toDo, task):
    """Delete a task."""
    if toDo is None or toDo.current_task_list is None:
        click.UsageError('Please load a list first.')
    else:
        if all:
            toDo.current_task_list.delete_all_tasks()
            click('The list is empty')
        else:
            if toDo.current_task_list.tasks.__len__() > 0 and int(task) <= toDo.current_task_list.tasks.__len__():
                click.echo('Deleted task: ' + toDo.current_task_list.tasks[int(task)-1].description)
                toDo.current_task_list.delete(int(task)-1)
            else:
                click.BadParameter('There is no task number {} in the list'.format(task))


@cli.command()
@click.option('--github_url', prompt='Github Url', default='http://github.com', help='Configure the github instnace to read and write your gist-to-do lists to.')
@click.option('--local_storage', prompt='Local Storage Folder', default='', help='Configure local storage location for your gist-to-do lists.')
@click.pass_obj
def config(toDo):
    """Configure options for cli."""
    click.echo('config')


@cli.command()
@click.pass_obj
def archive(toDo):
    """archive all checked tasks"""
    if toDo is None or toDo.current_task_list is None:
        click.UsageError('Please load a list first.')
    else:
        if toDo.current_task_list.tasks.__len__() > 0:
            click.echo('Archived tasks')
            toDo.current_task_list.archive()
        else:
            click.echo('There are no tasks to archive')

if __name__ == "__main__":
    print('run man')
    cli()