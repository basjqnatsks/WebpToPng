import asyncio
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from win10toast_click import ToastNotifier
import webbrowser

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop
        self.notifier = ToastNotifier()
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.webp'):
            print(f"File created: {event.src_path}")
            asyncio.run_coroutine_threadsafe(self.process_new_file(event.src_path), self.loop)
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.webp'):
            print(f"File modified: {event.src_path}")
            asyncio.run_coroutine_threadsafe(self.process_new_file(event.src_path), self.loop)
    def on_moved(self, event):
        if not event.is_directory and event.dest_path.endswith('.webp'):
            print(f"File moved/renamed: {event.dest_path}")
            asyncio.run_coroutine_threadsafe(self.process_new_file(event.dest_path), self.loop)
    async def process_new_file(self, filepath):
        print(f"New or modified .webp file detected: {filepath}")
        await self.convert_to_png(filepath)
    async def convert_to_png(self, filepath):
        try:
            print(f"Opening image file: {filepath}")
            img = Image.open(filepath)
            png_filename = filepath.replace('.webp', '.png')
            img.save(png_filename)
            print(f"Converted {filepath} to {png_filename}")
            self.show_clickable_notification(png_filename)
        except Exception as e:
            print(f"Failed to convert {filepath} to PNG: {e}")
    def show_clickable_notification(self, png_filename):
        def open_file():
            webbrowser.open(png_filename)
        self.notifier.show_toast(
            "Png Conversion Successful",
            f"Click to open: {os.path.basename(png_filename)}",
            duration=10,
            threaded=True,
            callback_on_click=open_file
        )
async def watch_directory(directory):
    loop = asyncio.get_event_loop()
    event_handler = NewFileHandler(loop)
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=False)
    observer.start()
    print(f"Started watching directory: {directory}")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
if __name__ == "__main__":
    directory_to_watch = "C:\\users\\%username%\\downloads"
    if not os.path.exists(directory_to_watch):
        print(f"Directory does not exist: {directory_to_watch}")
    else:
        print(f"Directory exists: {directory_to_watch}")
        asyncio.run(watch_directory(directory_to_watch))
