import http.server
import socketserver
import sys
import time
import imp


def get_response(handler, method, data):
    mimetype = "text/html"
    responseText = None
    path = handler.path
    request = handler.request
    # print(request)
    # print(path)

    fileContent = checkPaths(path)
    if fileContent != None:
        return fileContent, mimetype
    print("no file")

    scriptContent = checkScripts(path, request, method, data)
    if scriptContent != None:
        return scriptContent, mimetype

    print("no script")
    if(path == '/'):
        with open('main.html', 'r') as file:
            data = file.read().replace('\n', '')
            responseText = data
            #responseText = ''
    if path == '/exit':
        sys.exit()
    return responseText, mimetype


def checkScripts(path, request, method, data):
    for script in ["./"+path+".py", "./"+path+'/main.py']:
        try:
            return imp.load_source("temp", script).main(method, path, data, request)
        except FileNotFoundError:
            continue
    return None


def checkPaths(path):
    for p in ["./"+path, "./"+path+'/index.html', "./"+path+'.html']:
        response = checkPath(p)
        if response != None:
            #print("foudn for "+p)
            return response
        # else:
            #print("didndnt find for "+p)
    return None


def checkPath(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except NotADirectoryError:
        return None
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return None
