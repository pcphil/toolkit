from PIL import Image, ImageDraw, ImageOps
import os

class IconMaker:
    STANDARD_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

    @staticmethod
    def _get_unique_path(path):
        """Internal helper to increment filename if it exists."""
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path

    @staticmethod
    def generate_icon(input_path, output_path="output/icon.ico", circular=False, overwrite=True, custom_sizes=None):
        """
        Generates an ICO file with optional circular framing and overwrite control.
        """
        # 1. Handle File Path logic
        final_output = output_path if overwrite else IconMaker._get_unique_path(output_path)
        
        # 2. Determine sizes
        target_sizes = custom_sizes if custom_sizes else IconMaker.STANDARD_SIZES
        
        try:
            with Image.open(input_path).convert("RGBA") as img:
                # 3. Square Crop (Center)
                width, height = img.size
                min_dim = min(width, height)
                img = ImageOps.fit(img, (min_dim, min_dim), centering=(0.5, 0.5))

                # 4. Circular Mask
                if circular:
                    mask = Image.new('L', (min_dim, min_dim), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, min_dim, min_dim), fill=255)
                    img.putalpha(mask)

                # 5. Save
                img.save(final_output, format='ICO', sizes=target_sizes)
                print(f"✅ Success: Saved to '{final_output}'")

        except Exception as e:
            print(f"❌ Error: {e}")

    @staticmethod
    def make_border_circular(input_path, output_path="output/"):
        """
        Crops an image to a circle and saves it as a PNG to preserve transparency.
        """
        # Open the image and ensure it's in RGBA mode (supports transparency)
        img = Image.open(input_path).convert("RGBA")
        
        # 1. Square the image by cropping the center
        width, height = img.size
        size = min(width, height)
        left = (width - size) / 2
        top = (height - size) / 2
        right = (width + size) / 2
        bottom = (height + size) / 2
        img = img.crop((left, top, right, bottom))
        
        # 2. Create a mask for the circle
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # 3. Apply the mask to the alpha channel
        img.putalpha(mask)
        
        if output_path:
            # Must save as PNG to keep the transparent corners
            img.save(output_path, "PNG")
            
        return img