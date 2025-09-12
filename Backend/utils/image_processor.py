import os
import aiofiles
from PIL import Image, ImageFilter, ImageEnhance
from datetime import datetime
from starlette.datastructures import UploadFile


class ImageProcessor:
    def __init__(self):
        self.filter_dir = "uploads/filtered"
        os.makedirs(self.filter_dir, exist_ok=True)

    async def apply_filter(self, image_path: str, filter_type: str) -> str:
        """Apply filter to image and return the path to filtered image"""

        # Remove leading slash if exists for local file access
        local_path = image_path.lstrip("/")

        if not os.path.exists(local_path):
            raise ValueError(f"Image file not found: {local_path}")

        try:
            with Image.open(local_path) as img:
                # Convert to RGB if necessary
                if img.mode != "RGB":
                    img = img.convert("RGB")

                filtered_img = self._apply_filter_effect(img, filter_type)

                # Generate filtered image filename
                base_name = os.path.basename(image_path)
                name, ext = os.path.splitext(base_name)
                filtered_filename = f"{name}_{filter_type}{ext}"
                filtered_path = os.path.join(self.filter_dir, filtered_filename)

                # Save filtered image
                filtered_img.save(filtered_path, quality=85, optimize=True)

                return f"/uploads/filtered/{filtered_filename}"

        except Exception as e:
            raise ValueError(f"Failed to apply filter: {str(e)}")

    def _apply_filter_effect(self, img: Image.Image, filter_type: str) -> Image.Image:
        """Apply specific filter effect to image"""
        if filter_type == "none":
            return img
        elif filter_type == "vintage":
            return self._apply_vintage_filter(img)
        elif filter_type == "black_white":
            return self._apply_black_white_filter(img)
        elif filter_type == "sepia":
            return self._apply_sepia_filter(img)
        elif filter_type == "blur":
            return self._apply_blur_filter(img)
        elif filter_type == "sharpen":
            return self._apply_sharpen_filter(img)
        elif filter_type == "bright":
            return self._apply_brightness_filter(img)
        elif filter_type == "contrast":
            return self._apply_contrast_filter(img)
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")

    def _apply_vintage_filter(self, img: Image.Image) -> Image.Image:
        # Reduce saturation
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.7)

        # Add slight warm tint
        r, g, b = img.split()
        r = ImageEnhance.Brightness(r).enhance(1.1)
        g = ImageEnhance.Brightness(g).enhance(1.05)
        b = ImageEnhance.Brightness(b).enhance(0.9)

        return Image.merge("RGB", (r, g, b))

    def _apply_black_white_filter(self, img: Image.Image) -> Image.Image:
        return img.convert("L").convert("RGB")

    def _apply_sepia_filter(self, img: Image.Image) -> Image.Image:
        pixels = img.load()
        width, height = img.size

        for py in range(height):
            for px in range(width):
                r, g, b = pixels[px, py]

                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                pixels[px, py] = (min(255, tr), min(255, tg), min(255, tb))

        return img

    def _apply_blur_filter(self, img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.GaussianBlur(radius=2))

    def _apply_sharpen_filter(self, img: Image.Image) -> Image.Image:
        return img.filter(ImageFilter.SHARPEN)

    def _apply_brightness_filter(self, img: Image.Image) -> Image.Image:
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(1.3)

    def _apply_contrast_filter(self, img: Image.Image) -> Image.Image:
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.2)

    async def resize_image(
        self, image_path: str, max_width: int = 800, max_height: int = 800
    ) -> str:
        """Resize image while maintaining aspect ratio"""

        local_path = image_path.lstrip("/")

        if not os.path.exists(local_path):
            raise ValueError(f"Image file not found: {local_path}")

        try:
            with Image.open(local_path) as img:
                # Calculate new size maintaining aspect ratio
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                # Generate resized image filename
                base_name = os.path.basename(image_path)
                name, ext = os.path.splitext(base_name)
                resized_filename = f"{name}_resized{ext}"
                resized_path = os.path.join(
                    os.path.dirname(local_path), resized_filename
                )

                # Save resized image
                img.save(resized_path, quality=85, optimize=True)

                return f"/{resized_path}"

        except Exception as e:
            raise ValueError(f"Failed to resize image: {str(e)}")

    async def validate_image_file(self, filename: str, file_size: int):
        """Validate image file type and size"""

        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

        # Check file extension
        _, ext = os.path.splitext(filename.lower())
        if ext not in allowed_extensions:
            raise ValueError("Unsupported file type")

        if file_size > 20 * 1024 * 1024:  # 20MB limit
            raise ValueError("File size must be less than 20MB")

    def get_safe_filename(self, filename: str) -> str:
        """Generate safe filename by removing dangerous characters"""

        import re

        # Keep only alphanumeric characters, dots, and hyphens
        safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)

        # Add timestamp to avoid collisions
        name, ext = os.path.splitext(safe_name)
        timestamp = int(datetime.now().timestamp())

        return f"{name}_{timestamp}{ext}"

    async def write_file_and_get_image_path(
        self, file: UploadFile, upload_dir: str
    ) -> str:
        filename = self.get_safe_filename(file.filename)
        file_path = os.path.join(upload_dir, filename)

        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        return file_path
