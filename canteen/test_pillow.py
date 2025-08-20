from PIL import Image
import os


def save_test_image(output_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', 'tmp')) -> str:
    os.makedirs(output_dir, exist_ok=True)
    img = Image.new("RGB", (200, 200), color="red")
    output_path = os.path.join(output_dir, "pillow_test_red_square.jpg")
    img.save(output_path, format="JPEG")
    return output_path


if __name__ == "__main__":
    saved = save_test_image()
    print(f"Saved test image to: {saved}")
