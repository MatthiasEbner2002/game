import logging
#global LineCount
LineCount = 1
logLines = []
def debug(text):
    logLines.append(" " + str(LineCount) + ": " + text)
    #LineCount  += 1
    logging.debug(text)

def info(text):
    logLines.append(" " + str(LineCount) + ": " + text)
    #LineCount  += 1
    logging.info(text)

def error(text):
    logLines.append(" " + str(LineCount) + ": " + text)
    #LineCount += 1
    logging.error(text)