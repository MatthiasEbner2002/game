from threading import Thread, Lock
import threading
mutex = Lock()


def processData(data, thread_safe):
    if thread_safe:
        mutex.acquire()
    try:
        thread_id = threading.get_ident()
        print('\nProcessing data:', data, "ThreadId:", thread_id)
    finally:
        if thread_safe:
            mutex.release()


counter = 0
max_run = 100
thread_safe = True
while True:
    some_data = counter        
    t = Thread(target=processData, args=(some_data, thread_safe))
    t.start()
    counter = counter + 1
    if counter >= max_run:
        break