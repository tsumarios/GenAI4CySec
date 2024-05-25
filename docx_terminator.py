import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DocxDeletionHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".docx"):
            try:
                os.remove(event.src_path)
                print(f"Deleted: {event.src_path}")
            except Exception as e:
                print(f"Failed to delete {event.src_path}: {e}")


def run_daemon(directory_to_watch):
    event_handler = DocxDeletionHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    directory_to_watch = "./docs_folder/"
    run_daemon(directory_to_watch)
