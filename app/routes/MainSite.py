from flask import Blueprint, render_template, request

# database
from app.models.GalleryModel import Gallery
from app.resources.ConcertsResource import get_planned_concerts, get_past_concerts
from app.resources.GalleriesResource import get_all_galleries, get_gallery_by_secure_title
from app.resources.SlidesResource import get_all_slides
from app.resources.TextsResource import get_text_by_page

mainSite = Blueprint('mainSite', __name__)


@mainSite.route('/')
def index():
    closest_concerts = get_planned_concerts(3)
    slides = get_all_slides()

    return render_template('index.html',
                           closest_concerts=closest_concerts,
                           slides=slides
                           )


@mainSite.route('/onas/czzk')
def about_czzk():
    page = 'czzk'
    chapters = get_text_by_page(page)

    return render_template('about-czzk.html',
                           chapters=chapters
                           )


@mainSite.route('/onas/muzyka')
def about_music():
    page = 'muzyka'
    chapters = get_text_by_page(page)
    return render_template('about-music.html',
                           chapters=chapters)
# TODO get albums


@mainSite.route('/onas/kazik')
def about_kazik():
    return render_template('about-kazik.html')


@mainSite.route('/koncerty')
def concerts():
    planned_concerts = get_planned_concerts()
    past_concerts = get_past_concerts()

    return render_template('concerts.html',
                           planned_concerts=planned_concerts,
                           past_concerts=past_concerts
                           )


@mainSite.route('/multimedia/audio')
def multimedia_audio():
    return render_template('multimedia-audio.html')


@mainSite.route('/multimedia/galeria')
def multimedia_galleries():
    page = request.args.get('strona', 1, type=int)

    galleries = get_all_galleries(page)

    return render_template('multimedia-galleries.html',
                           galleries=galleries
                           )


@mainSite.route('/multimedia/galeria/<string:gallery_secure_title>')
def multimedia_specific_gallery(gallery_secure_title):
    gallery = get_gallery_by_secure_title(gallery_secure_title)
    photos = Gallery.get_photos(gallery)

    return render_template('multimedia-specific-gallery.html',
                           gallery=gallery,
                           photos=photos)


@mainSite.route('/multimedia/gadzety')
def multimedia_merch():
    return render_template('multimedia-merch.html')


@mainSite.route('/multimedia/archiwum')
def multimedia_archive():
    return render_template('multimedia-archive.html')


@mainSite.route('/kontakt')
def contact():
    return render_template('contact.html')
