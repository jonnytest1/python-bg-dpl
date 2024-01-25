import datetime


def log_line(line: str):
    with open("inputpy.log", "a") as myfile:
        myfile.write(datetime.datetime.now().isoformat()+":"+line+"\n")
