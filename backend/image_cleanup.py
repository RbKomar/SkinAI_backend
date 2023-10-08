import os
import time

IMAGE_STORAGE_PATH = "database/images"
CLEANUP_INTERVAL = 86400  # 24 hours in seconds
MAX_IMAGE_AGE = 604800  # 7 days in seconds


def cleanup_old_images():
    current_time = time.time()

    for image_file in os.listdir(IMAGE_STORAGE_PATH):
        image_path = os.path.join(IMAGE_STORAGE_PATH, image_file)
        file_age = current_time - os.path.getmtime(image_path)

        if file_age > MAX_IMAGE_AGE:
            os.remove(image_path)
            print(f"Deleted old image: {image_file}")


if __name__ == "__main__":
    while True:
        cleanup_old_images()
        time.sleep(CLEANUP_INTERVAL)
