from pathlib import Path

import pillow_avif  # noqa
import wrapt
from willow.image import INITIAL_IMAGE_CLASSES, ImageFile
from willow.plugins.pillow import PillowImage, _PIL_Image
from willow.registry import registry

try:
    import imghdr

    @wrapt.patch_function_wrapper(imghdr, "what")
    def what(wrapped, instance, args, kwargs):
        result = wrapped(*args, **kwargs)

        return Path(args[0].name).suffix[1:] if result is None else result

except ModuleNotFoundError:
    pass


class AVIFImageFile(ImageFile):
    format_name = "avif"


def pillow_save_avif(image, filename, quality=50, **options):
    image.get_pillow_image().save(filename, "avif", quality=quality, **options)
    return AVIFImageFile(filename)


def avif_to_pillow(image_file):
    image_file.f.seek(0)
    image = _PIL_Image().open(image_file.f)
    image.load()

    return PillowImage(image)


registry.register_image_class(AVIFImageFile)
registry.register_operation(PillowImage, "save_as_avif", pillow_save_avif)
registry.register_converter(AVIFImageFile, PillowImage, avif_to_pillow)

INITIAL_IMAGE_CLASSES["avif"] = AVIFImageFile
