import pathlib

import pillow_avif  # noqa
import wrapt
from willow.image import INITIAL_IMAGE_CLASSES, ImageFile
from willow.plugins.pillow import PillowImage
from willow.registry import registry

try:
    import imghdr

    @wrapt.patch_function_wrapper(imghdr, "what")
    def what(wrapped, instance, args, kwargs):
        result = wrapped(*args, **kwargs)

        return pathlib.Path(args[0].name).suffix[1:] if result is None else result

except ModuleNotFoundError:
    pass


class AVIFImageFile(ImageFile):
    format_name = "avif"


def pillow_save_avif(image, filename, quality=50, **options):
    image.get_pillow_image().save(filename, "avif", quality=quality, **options)
    return AVIFImageFile(filename)


registry.register_operation(PillowImage, "save_as_avif", pillow_save_avif)
INITIAL_IMAGE_CLASSES["avif"] = AVIFImageFile
