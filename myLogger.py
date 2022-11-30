import logging
LineCount = 1
logLines = []
error_text = "ERROR"
info_text = "INFO "
debug_text = "DEBUG"


def debug(text):
    global LineCount
    logLines.append(debug_text + "(" + str(LineCount) + "): " + text)
    LineCount += 1
    logging.debug(text)


def info(text):
    global LineCount
    logLines.append(info_text + "(" + str(LineCount) + "): " + text)
    LineCount += 1
    logging.info(text)


def error(text):
    global LineCount
    logLines.append(error_text + "(" + str(LineCount) + "): " + text)
    LineCount += 1
    logging.error(text)
