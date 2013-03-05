#!/usr/bin/env python
import os, time, subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_PATHS = [
    os.path.join(os.path.dirname(__file__), p)
    for p in ['templates', 'static']
]
MAKE_PAGES = os.path.join(os.path.dirname(__file__), 'make_pages.py')

class MyFileSystemEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        res = subprocess.call(['./'+MAKE_PAGES])
        print '\n EVENT:', event
        print 'make_pages.py returned', res
        

if __name__ == "__main__":
    event_handler = MyFileSystemEventHandler()
    observer = Observer()
    for p in WATCH_PATHS:
        observer.schedule(event_handler, path=p, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

