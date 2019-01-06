#
#
# pip install click
# pip install colorama
# pip install nipyapi
# pip install prompt_toolkit

#
from prompt_toolkit import prompt
import nipyapi
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import click
import time

nipyapi.config.nifi_config.host = "http://35.231.236.230:8080/nifi-api"
processors = {}

@click.group()
def greet():
    pass

@greet.command()
@click.argument('name')  # add the name argument
def hello(**kwargs):
    print('Hello, {0}!'.format(kwargs['name']))


def handle_start_stop_processor(user_input):
    splits = user_input.split()
    proc_index = splits[1] if len(splits) >= 2 else "all"

    if proc_index.lower() == "all":
        processor_list = nipyapi.canvas.list_all_processors()
        for p in processor_list:
            start_stop_processor(p,user_input)
    elif proc_index.isdigit:
        p = processors[proc_index]
        if p is None:
            print("Not a valid processor")
            return
        start_stop_processor(p,user_input)
    else:
        print("Not a valid processor index: %s" % proc_index)


def start_stop_processor(processor, user_input):
    is_start = True if user_input.startswith("startp") else False

    p = get_processor(processor.id)
    prev_status = "Running" if not is_start else "Stopped"
    after_status = "Running" if is_start else "Stopped"
    if p.status.run_status != prev_status:
        print("Processor (%s) is not %s:" % ( processor.component.name,prev_status))
        return

    if is_start:
        print("Starting processor %s(%s):" %(p.component.name,p.id))
    else:
        print("Stopping processor %s(%s):" %(p.component.name,p.id))
    nipyapi.canvas.schedule_processor(processor,is_start)
    p = get_processor(processor.id)
    time_out = 10

    start_time = time.time()
    while p.status.run_status != after_status:
        time.sleep(0.1)
        if (time.time() - start_time ) > time_out:
            print("Processor is not %s after %d seconds, current status is: %s" % (after_status,time_out,p.status.run_status))
            return
    print("Processor is %s." % after_status)


def get_processor(id):
    p =  nipyapi.canvas.get_processor(id,"id")
    if p is None:
        print("No processor found for id: %s" % id)
    return p


def list_processors(user_input):
    name = None
    splits = user_input.split()
    if len(splits) > 1:
        name = splits[1]


    pg_id = nipyapi.canvas.get_root_pg_id()
    #print(pg_id)
    processor_list = nipyapi.canvas.list_all_processors()

    procCount = len(processors)
    index = 1
    processors.clear()
    for p in processor_list:
        if (name is not None and name.lower() in p.component.name.lower()) or name is None:
            print(str(index) + ".  " + p.id + " " + p.component.name + " " + p.status.run_status)
            #print(p.component.name)
            processors[ str(index) ] = p
            index = index + 1


def main():
    welcome = "---- Welcome to Nifi command line ----"
    help = """
              lsp [name]  -- List processors
              startp [index] -- start processor[s], if no index is provided , start all processors"
              stopp  [index] -- stop processor[s], if no index is provided, stop all processor"
              exit -- exit command line
    """
    print(welcome)
    print(help)
    while 1:
        user_input = prompt('Nifi>'
                           ,history = FileHistory("history.txt")
                           , auto_suggest=AutoSuggestFromHistory()
                           )
        if user_input == "exit":
            break
        elif user_input.startswith("lsp"):
            list_processors(user_input)
        elif user_input.startswith("stopp") or user_input.startswith("startp"):
            handle_start_stop_processor(user_input)
        elif user_input == "clear":
            click.clear()
        else:
            print("Not supported command")

        #print(user_input)


if __name__ == "__main__":
    main()