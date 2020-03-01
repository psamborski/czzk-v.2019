import time
from os import listdir, path
from os.path import isfile, join
from flask import abort

from app import UPLOAD_FOLDER
from app.models.functions import get_yt_video_id


class Gallery:
    def __init__(self, gallery):
        """
        Gallery class has database object parameter:
        :param gallery:
        """
        self.id = str(gallery.id)
        self.title = gallery.title
        self.secure_title = gallery.secure_title
        self.thumbnail_file = gallery.thumbnail_file
        self.videos = gallery.videos
        self.author = gallery.author

    def get_photos(self):
        """
        Get gallery photos by its directory.
        :return Photos list:
        """
        directory = UPLOAD_FOLDER + '/images/galleries/' + self.id
        photos = [f for f in listdir(directory) if isfile(join(directory, f))]
        photos.sort(key=lambda x: path.getmtime(directory + '/' + x))
        # sort files by creation date; display creation date of each file
        # for photo in photos:
        #     print(photo + ' ' + time.strftime('%d/%m/%Y', time.gmtime(path.getmtime(directory + '/' + photo))))

        return photos

    def paginate_photos(self, page, items_per_page=9):
        photos = self.get_photos()

        paginated_photos = [photos[i:i + items_per_page] for i in range(0, len(photos), items_per_page)]
        # https://stackoverflow.com/questions/3950079/paging-python-lists-in-slices-of-4-items

        try:
            page_photos = paginated_photos[page - 1]
        except IndexError:
            abort(404)

        all_pages = [i for i in range(1, len(paginated_photos)+1)]

        has_prev = False if page == 1 else True
        has_next = False if page == all_pages[-1] else True

        prev_num = page - 1 if has_prev else 1
        next_num = page + 1 if has_next else 1

        return dict(
            page_photos=page_photos,
            current_page=page,
            all_pages=all_pages,
            has_prev=has_prev,
            has_next=has_next,
            prev_num=prev_num,
            next_num=next_num
                    )

    def get_videos(self):
        videos = self.videos

        videos_list = []

        if videos:
            for link in videos.split(','):
                video_id = get_yt_video_id(link.strip())
                videos_list.append({
                    "link": link.strip(),
                    "id": video_id,
                    "thumbnail": f"https://img.youtube.com/vi/{video_id}/0.jpg"
                })

        return videos_list
