#
#  Click
# pip install click
# pip install colorama
#
from prompt_toolkit import prompt
import nipyapi
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import click

@click.group()
def greet():
    pass

@greet.command()
@click.argument('name')  # add the name argument
def hello(**kwargs):
    print('Hello, {0}!'.format(kwargs['name']))


def list_processors():
    nipyapi.config.nifi_config.host = "http://35.231.236.230:8080/nifi-api"
    pg_id = nipyapi.canvas.get_root_pg_id()
    print(pg_id)
    processors = nipyapi.canvas.list_all_processors()
    procCount = len(processors)
    for p in processors:
        print(p.id + " " + p.component.name + " " + p.status.run_status)
    
while 1:
    user_input = prompt('Nifi>'
                       ,history = FileHistory("history.txt")
                       , auto_suggest=AutoSuggestFromHistory()
                       )
    if user_input == "exit":
        break
    elif user_input == "listp":
        list_processors()
    elif user_input == "clear":
        click.clear()
    elif user_input.startswith("greet"):
        hello()
        
    print(user_input)