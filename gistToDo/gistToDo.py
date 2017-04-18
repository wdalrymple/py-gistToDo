import click
from gistToDo.todoList import item
from gistToDo.todoList import itemList

@click.group()
def cli():
    """
    gist-to-do is a CLI for managing a To-Do list backed against a users github Gist's
    """

@cli.command()
def login():
    """Login with your github credentials (userid/password). These are cached locally."""
    click.echo('login')

@cli.command()
def whoami():
    """Ouput the userid of the currently logged in user"""
    click.echo('whoami')

@cli.command()
def list():
    """List known gists that follow the pattern gistToDo-{title}.md"""
    click.echo('list')

@cli.command()
def show():
    """Display the current ToDo list loaded"""
    click.echo('show')

@cli.command()
def create():
    """Create a new ToDo List"""
    click.echo('create')

@cli.command()
def add():
    """Add a new task"""
    click.echo('add')
    l = itemList('Test this out woo hooooo')

    l.tasks.append(item('item 1'))
    l.tasks.append(item('item 2'))
    l.tasks.append(item('item 3'))
    l.tasks.append(item('item 4'))
    print(l.__format__())

@cli.command()
def check():
    """Check/Uncheck tasks in the current list"""
    click.echo('check')

@cli.command()
def load():
    """Load and set a ToDo list from known gists that follow the pattern gistToDo-{title}.md"""
    click.echo('load')

@cli.command()
def delete():
    """Delete a task."""
    click.echo('delete')

@cli.command()
def config():
    """Configure options for cli."""
    click.echo('config')

@cli.command()
def archive():
    """archive all checked tasks"""
    click.echo('archive')
