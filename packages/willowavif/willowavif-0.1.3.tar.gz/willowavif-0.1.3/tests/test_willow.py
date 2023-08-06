import os

from willow.image import Image, UnrecognisedImageFormatError

import willowavif  # noqa


def test_converts_images(image_diff, image_regression):
    base_path = os.path.dirname(__file__)
    from_path = os.path.abspath(os.path.join(base_path, "from"))
    to_path = os.path.abspath(os.path.join(base_path, "to"))

    for filename in os.listdir(from_path):
        in_path = os.path.join(from_path, filename)
        with open(in_path, "rb") as f:
            try:
                i = Image.open(f)
            except UnrecognisedImageFormatError as e:
                print(f"Failed to load {filename}")
                raise e

            out_avif = os.path.join(to_path, f"{filename}.avif")

            with open(out_avif, "wb") as fout:
                i.save_as_avif(fout)

            assert image_regression(out_avif, threshold=0.5, suffix=filename)
