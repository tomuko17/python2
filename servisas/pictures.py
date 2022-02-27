import secrets, os
from PIL import Image
from servisas import app


def save_picture(form_picture):
    random_name = secrets.token_urlsafe(32)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_name + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilio_nuotraukos', picture_fn)

    output_size = (200, 200)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


