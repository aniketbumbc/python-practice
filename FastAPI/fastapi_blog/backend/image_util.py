from io import BytesIO
from PIL import Image, ImageOps


def process_profile_image(content: bytes) -> bytes:
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)
        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])  # use alpha as mask
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, "JPEG", quality=85, optimize=True)
        return buffer.getvalue()


def process_blog_thumbnail(content: bytes) -> bytes:
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)
        img = ImageOps.fit(img, (800, 450), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])  # use alpha as mask
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, "JPEG", quality=85, optimize=True)
        return buffer.getvalue()