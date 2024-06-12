import os
import random
from PIL import Image
import io
import base64

def get_alphabet_images(phrase, alphabet_directory):
    images = []
    for char in phrase:
        char = char.lower()
        if char.isalpha():
            char_dir = os.path.join(alphabet_directory, char)
            if os.path.exists(char_dir) and os.path.isdir(char_dir):
                # Get a random image from the alphabet subdirectory
                image_files = [f for f in os.listdir(char_dir) if f.endswith(('png', 'jpg', 'jpeg'))]
                if image_files:
                    image_path = os.path.join(char_dir, random.choice(image_files))
                    with Image.open(image_path) as img:
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        images.append(f"data:image/png;base64,{img_str}")
    return images


def handle_phrase(phrase, video_directory, alphabet_directory):
    # Normalize the phrase to lower case and replace spaces with underscores
    normalized_phrase = phrase.lower().replace(' ', '_')

    # Check if a corresponding video exists
    video_file = os.path.join(video_directory, f"{normalized_phrase}.mp4")

    if os.path.exists(video_file):
        return {"type": "video", "data": f"{normalized_phrase}.mp4"}

    # If no video, return images of individual letters
    images = get_alphabet_images(normalized_phrase, alphabet_directory)
    if images:
        return {"type": "images", "data": images}

    # If neither exists, return an error
    return {"type": "error", "message": "No corresponding video or images found."}
