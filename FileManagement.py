from os import scandir,rename
from os.path import splitext,exists,join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


desktop_dir = "/Users/boydjenkins/Desktop"
source_dir = "/Users/boydjenkins/Downloads"
dest_dir_sfx = "/Users/boydjenkins/Desktop/Sound"
dest_dir_music = "/Users/boydjenkins/Desktop/Music"
dest_dir_video = "/Users/boydjenkins/Desktop/Downloaded Videos"
dest_dir_image = "/Users/boydjenkins/Desktop/Downloaded Images"
dest_dir_documents = "/Users/boydjenkins/Desktop/Downloaded Documents"
dest_dir_screenshots = "/Users/boydjenkins/Desktop/ScreenShots"

# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

def make_unique(dest,name):
    filename,extension = splitext(name)
    counter = 1

    #if file exists, add number to the end of the filename
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest,entry,name):
    full_dest_path = join(dest,name)
    if exists(full_dest_path):
        unique_name = make_unique(dest,name)
        full_dest_path = join(dest,unique_name)
    move(entry.path,full_dest_path)

class MoverHandler(FileSystemEventHandler):
    #This function will run whenever there is a change in "source directory"
    #.upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with scandir(source_dir) as entries_download,scandir(desktop_dir) as entries_desktop:
            for entry in entries_download:
                name = entry.name
                self.check_audio_files(entry,name)
                self.check_video_files(entry,name)
                self.check_image_files(entry,name)
                self.check_document_files(entry,name)
            for entry in entries_desktop:
                name = entry.name
                self.check_screenshot_files(entry,name)


    def check_audio_files(self,entry,name):
        for extensions in audio_extensions:
            if name.endswith(extensions) or name.endswith(extensions.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest,entry,name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self,entry,name):
        for extensions in video_extensions:
            if name.endswith(extensions) or name.endswith(extensions.upper()):
                move_file(dest_dir_video,entry,name)
                logging.info(f"Moved video file: {name}")


    def check_image_files(self,entry,name):
        for extensions in image_extensions:
            if name.endswith(extensions) or name.endswith(extensions.upper()):
                move_file(dest_dir_image,entry,name)
                logging.info(f"Moved image file: {name}")


    def check_document_files(self,entry,name):
        for extension in document_extensions:
            if name.endswith(extension) or name.endswith(extension.upper()):
                move_file(dest_dir_documents,entry,name)
                logging.info(f"Moved document file: {name}")
                

    def check_screenshot_files(self,entry,name):
        if name.startswith("Screenshot"):
            move_file(dest_dir_screenshots,entry,name)
            logging.info(f"Moved Screenshots file: {name}")


def main():
    logging.basicConfig(level=logging.INFO,
                        format = '%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler,source_dir,recursive=True)
    observer.schedule(event_handler,desktop_dir, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()