print("Hello, world!")
import nipyapi
def main():
    nipyapi.config.nifi_config.host = "http://35.231.236.230:8080/nifi-api"
    pg_id = nipyapi.canvas.get_root_pg_id()
    print(pg_id)
    processors = nipyapi.canvas.list_all_processors()
    procCount = len(processors)
    for p in processors:
        print(p.id + " " + p.component.name + " " + p.status.run_status)
        if p.status.run_status == "Stopped":
            nipyapi.canvas.schedule_processor(p,True,True)
    #print(procCount)

if __name__ == "__main__":
    main()    