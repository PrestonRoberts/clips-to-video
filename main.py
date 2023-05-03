import os
import re
from moviepy.editor import *

# Class for storing clip information
class Clip:
    def __init__(self, file_location, file_name, title):
        self.file_location = file_location
        self.file_name = file_name
        self.title = title

    def display_clip_information(self):
        print("File Location: " + self.file_location)
        print("File Name: " + self.file_name)
        print("Clip Title: " + self.title)

# Remove starting and ending quotes from a file
def remove_quotes(file_path):
    if file_path.startswith('"') and file_path.endswith('"'):
        file_path = file_path[1:-1]
    return file_path

# Check if file exists and has a .mp4 extension
def is_mp4_file(file_path):
    if not os.path.exists(file_path):
        return False
    _, extension = os.path.splitext(file_path)
    if extension.lower() != ".mp4":
        return False
    
    return True

# Get the name of the file from the path
def get_file_name(file_path):
    filename = os.path.basename(file_path)
    base_name = os.path.splitext(filename)[0]
    return [filename, base_name]

# Yes or no question
def yes_no_question(question):
    choice = ''
    while True:
        choice = input(question + (" (y/n): "))
        if choice != 'y' and choice != 'n':
            print('Response not valid')
        else:
            break
    
    if choice == 'y':
        return 'yes'
    
    return 'no'

# Get user clip file locations
def get_clips():
    clips = [];

    is_done = False;
    while(not is_done):
        video_path = input("Enter the file path of your clip: ")
        video_path = remove_quotes(video_path)

        if is_mp4_file(video_path):
            print("Clip added")
            file_name, title = get_file_name(video_path)
            clips.append(Clip(video_path, file_name, title))
        else:
            print("File path not valid")

        choice = yes_no_question('Do you want to upload another clip?')
        
        if choice != 'yes':
            print(choice)
            is_done = True;

    return clips

# Change the titles of clips
def change_titles(clips):
    choice = yes_no_question("Do you want to update the titles of the clips?")
    if choice != 'yes':
        print('The clip titles will not be changed')
        return 0
    
    for clip in clips:
        print('==========')
        clip.display_clip_information()
        new_title = input("Enter the new title: ")

        # Double check
        is_good = False
        while(not is_good):
            choice = yes_no_question("Is '" + new_title + "' the title that you want?")
            
            if choice != 'yes':
                new_title = input("Enter the new title: ")
            else:
                is_good = True
        
        clip.title = new_title
        print("'" + new_title + "' is the new title")

# Get the input from the user as to where the titles will be placed
def get_location():
    title_location = ()
    while(True):
        choice = input("Where do you want the title of the clips to be (top left/top right/bottom left/bottom right): ")
        if choice == 'top left':
            title_location = ('left', 'top')
            break

        elif choice == 'top right':
            title_location = ('right', 'top')
            break

        elif choice == 'bottom left':
            title_location = ('left', 'bottom')
            break

        elif choice == 'bottom right':
            title_location = ('right', 'bottom')
            break

        else:
            print('That is not a valid location.')

    return title_location

# Get the input from the user as to how long titles should be displayed
def get_duration():
    while True:
        try:
            number = int(input("How many seconds should the titles be displayed on the clip? (-1 for the whole clip): "))
            if number >= 0 or number == -1:
                return number
            else:
                print("Invalid duration.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Get the input from the user for the font size of the title
def get_title_size():
    while True:
        try:
            number = int(input("What should the title fontsize be?: "))
            if number > 0:
                return number
            else:
                print("Invalid size.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Check if color is valid
def is_valid_hex_color(color_string):
    hex_color_regex = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})([A-Fa-f0-9]{2})?$')
    return bool(hex_color_regex.match(color_string))

# Get the input from the user for the font color of the title
def get_title_color():
    while True:
        color = input("What color should the title be? (hex color): ")

        if is_valid_hex_color(color):
            return color
        
        else:
            print('Not a valid hex color')

# Get the input from the user for the title outline color
def get_stroke_color():
    color = '#fff'
    size = 0

    while True:
        color = input("What color should the outline be? (hex color): ")

        if is_valid_hex_color(color):
            break
        
        else:
            print('Not a valid hex color')

    while True:
        try:
            size = float(input("What size should the stroke be?: "))
            if size > 0:
                break
            else:
                print("Invalid size.")
        except ValueError:
            print("Invalid input.")

    return color, size

# Testing functions
def display_clips_test(clips):
    for clip in clips:
        print("==========")
        clip.display_clip_information()
        print("==========")

    return 0

# Main function
def main():
    # Get user input clips
    clips = get_clips()
    display_clips_test(clips) # debugging

    # Handle titles
    include_titles = False
    title_location = ()
    title_duration = 0
    title_size = 0
    title_color = '#fff'

    stroke_color = "#fff"
    stroke_width = 0

    choice = yes_no_question("Do you want to include titles of clips in the video?");
    if choice == 'yes':
        include_titles = True
        change_titles(clips)
    elif choice == 'no':
        include_titles = False

    display_clips_test(clips) # debugging

    if include_titles:
        # location of titles
        title_location = get_location()

        # duration of titles
        title_duration = get_duration()

        # title size
        title_size = get_title_size()

        # title color
        title_color = get_title_color()

        # stroke color
        choice = yes_no_question("Do you want the text to have an outline?");
        if choice == 'yes':
            stroke_color, stroke_width = get_stroke_color()

    display_clips_test(clips) # debugging

    # Load all videos
    all_movies = []
    for clip in clips:
        movie = VideoFileClip(clip.file_location)

        # Title
        if include_titles:
            txt_clip = TextClip(txt=clip.title, fontsize=title_size, color=title_color, stroke_color=stroke_color, stroke_width=stroke_width)
            txt_clip = txt_clip.set_position(title_location).set_duration(min(movie.duration, title_duration))
            movie = CompositeVideoClip([movie, txt_clip])
        
        all_movies.append(movie)

    
    # Export
    final_video = concatenate_videoclips(all_movies)
    final_video.write_videofile("final_video.mp4")

if __name__ == '__main__':
    main()