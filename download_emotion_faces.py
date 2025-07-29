import os
import urllib.request

# Directory to save images
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'django_backend', 'static', 'emotional_faces')
os.makedirs(STATIC_DIR, exist_ok=True)

# Demo URLs (public domain or free for academic use)
IMAGES = {
    'happy1.jpg': 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Smile_Face.png',
    'happy2.jpg': 'https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg',
    'sad1.jpg': 'https://upload.wikimedia.org/wikipedia/commons/0/0a/Sad_Face.png',
    'sad2.jpg': 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Sad_face_icon.png',
    'angry1.jpg': 'https://upload.wikimedia.org/wikipedia/commons/6/6e/Angry_Face.png',
    'angry2.jpg': 'https://upload.wikimedia.org/wikipedia/commons/2/2e/Angry_face_icon.png',
    'fear1.jpg': 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Fearful_Face.png',
    'fear2.jpg': 'https://upload.wikimedia.org/wikipedia/commons/7/7e/Fear_face_icon.png',
    'surprise1.jpg': 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Surprised_Face.png',
    'disgust1.jpg': 'https://upload.wikimedia.org/wikipedia/commons/3/3b/Disgusted_Face.png',
}

for filename, url in IMAGES.items():
    out_path = os.path.join(STATIC_DIR, filename)
    if not os.path.exists(out_path):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, out_path) 
    else:
        print(f"{filename} already exists, skipping.")

print("All images downloaded to:", STATIC_DIR)