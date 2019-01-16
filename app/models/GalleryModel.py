from os import listdir
from os.path import isfile, join

from app import UPLOAD_FOLDER


class Gallery:
    def __init__(self, gallery):
        """
        Gallery class has database object parameter:
        :param gallery:
        """
        self.title = gallery.title
        self.secure_title = gallery.secure_title
        self.thumbnail = gallery.thumbnail

    def get_photos(self):
        """
        Get gallery photos by its directory.
        :return Photos list:
        """
        directory = UPLOAD_FOLDER + '/galleries/' + self.secure_title
        photos = [f for f in listdir(directory) if isfile(join(directory, f))]

        return photos
