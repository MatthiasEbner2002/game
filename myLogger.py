import logging
LineCount = 1
logLines = []


def debug(text):
    global LineCount
    logLines.append("DEBUG(" + str(LineCount) + "): " + text)
    LineCount += 1
    logging.debug(text)


def info(text):
    global LineCount
    logLines.append("INFO (" + str(LineCount) + "): " + text)
    LineCount += 1
    logging.info(text)


def error(text):
    global LineCount
    logLines.append("ERROR(" + str(LineCount) + "): " + text)
    LineCount += 1
    logging.error(text)
