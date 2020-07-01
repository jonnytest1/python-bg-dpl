from customlogging import logKibana

try:
    None.test()
except Exception as e:
    logKibana("ERROR", "tet", e)
    print("back from logging")
