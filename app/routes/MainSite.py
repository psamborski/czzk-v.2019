from flask import Blueprint, render_template, request
from itertools import groupby

# database
from app.models.GalleryModel import Gallery
from app.resources.AlbumsResource import get_all_albums
from app.resources.ConcertsResource import get_planned_concerts, get_past_concerts
from app.resources.GalleriesResource import get_all_galleries, get_gallery_by_secure_title
from app.resources.SlidesResource import get_all_slides
from app.resources.TextsResource import get_text_by_page

MainSite = Blueprint('MainSite', __name__)


@MainSite.route('/')
def index():
    closest_concerts = get_planned_concerts(3)
    slides = get_all_slides()

    return render_template('index.html',
                           closest_concerts=closest_concerts,
                           slides=slides
                           )


@MainSite.route('/onas/czzk')
def about_czzk():
    page = 'czzk'
    chapters = get_text_by_page(page)

    return render_template('about-czzk.html',
                           chapters=chapters
                           )


@MainSite.route('/onas/muzyka')
def about_music():
    page = 'muzyka'
    chapters = get_text_by_page(page)
    albums = get_all_albums()
    if albums:
        albums = groupby(albums, lambda x: x.year)

    # for key, group in groupby(albums, lambda x: x.year):
    #     print(key)
    #     for album in group:
    #         print(album.title)
    # https://stackoverflow.com/questions/45732065/group-list-by-some-value-in-python
    # https://stackoverflow.com/questions/773/how-do-i-use-pythons-itertools-groupby
    # the other idea: make a dict ({year=[album1, album2]})

    return render_template('about-music.html',
                           chapters=chapters,
                           albums=albums
                           )


@MainSite.route('/onas/kazik')
def about_kazik():
    return render_template('about-kazik.html')


@MainSite.route('/koncerty')
def concerts():
    planned_concerts = get_planned_concerts()
    past_concerts = get_past_concerts()

    return render_template('concerts.html',
                           planned_concerts=planned_concerts,
                           past_concerts=past_concerts
                           )


@MainSite.route('/multimedia/audio')
def multimedia_audio():
    return render_template('multimedia-audio.html')


@MainSite.route('/multimedia/galeria')
def multimedia_galleries():
    page = request.args.get('strona', 1, type=int)

    galleries = get_all_galleries(page)

    return render_template('multimedia-galleries.html',
                           galleries=galleries
                           )


@MainSite.route('/multimedia/galeria/<string:gallery_secure_title>')
def multimedia_specific_gallery(gallery_secure_title):
    page = request.args.get('strona', 1, type=int)

    gallery = Gallery(get_gallery_by_secure_title(gallery_secure_title))
    paginated_photos = gallery.paginate_photos(page=page)

    return render_template('multimedia-specific-gallery.html',
                           gallery=gallery,
                           paginated_photos=paginated_photos)


@MainSite.route('/multimedia/gadzety')
def multimedia_merch():
    return render_template('multimedia-merch.html')


@MainSite.route('/multimedia/archiwum')
def multimedia_archive():
    return render_template('multimedia-archive.html')


@MainSite.route('/kontakt')
def contact():
    return render_template('contact.html')
