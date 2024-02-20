# main.py

from video_generator.script import generate_script
from video_generator.audio import generate_audio
from video_generator.media import retrieve_images
from video_generator.video import curate_video

# Define the main function
def main():
    # Prompt the user to input the desired animal
    animal = input("Animal: ")
    
    # Generate and retrieve the script, audio, and images
    script = generate_script(animal)
    audio = generate_audio(script)
    images = retrieve_images(animal)
    
    # Curate the video using the generated script, audio, and retrieved images
    curate_video(animal, script, audio, images)


if __name__ == "__main__":
    main()
