# main.py

import os
import shutil
from video_generator.script import generate_script
from video_generator.audio import generate_audio
from video_generator.images import retrieve_images
from video_generator.video import curate_video

def setup():
    """
    Set up the video directory by taking user input for the animal.
    If the directory already exists, delete it and create a new one.

    Returns:
    - str: The user-inputted animal name.
    """
    # Take user input for the animal name
    animal_input = input("Animal: ")
    file_path = f"./videos/{animal_input}"

    # If the directory already exists, delete it
    if os.path.exists(file_path):
        shutil.rmtree(file_path)

    # Create a new directory
    os.makedirs(file_path)
    print("Successfully setup video directory!")

    # Return the animal name
    return animal_input


def main():
    """
    The main function that orchestrates the video creation process.
    Calls functions to generate script, audio, retrieve images, and curate the video.
    """
    # Set up the video directory
    animal = setup()

    # Generate script, audio, and retrieve images
    script = generate_script(animal, word_count=1000)
    audio = generate_audio(script)
    images = retrieve_images(animal, image_count=30)

    # Curate the video using generated script, audio, and images
    curate_video(animal, script, audio, images)


if __name__ == "__main__":
    main()
