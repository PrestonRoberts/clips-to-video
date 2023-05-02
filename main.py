import os

class Clip:
    def __init__(self, file_location, title):
        self.file_location = file_location
        self.title = title

    def display_clip_information(self):
        print("File Locaiton: " + self.file_location)
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
def get_filename(file_path):
    filename = os.path.basename(file_path)
    base_name = os.path.splitext(filename)[0]
    return base_name

# Get user clip file locations
def get_clips():
    clips = [];

    is_done = False;
    while(not is_done):
        video_path = input("Enter the file path of your clip: ")
        video_path = remove_quotes(video_path)

        if is_mp4_file(video_path):
            print("Clip added")
            clips.append(Clip(video_path, get_filename(video_path)))
        else:
            print("File path not valid")

        choice = input("Do you want to upload another clip? (yes/anything else): ")
        
        if choice != 'yes':
            print(choice)
            is_done = True;

    return clips

# Change the titles of clips
def change_titles(clips):
    choice = input("Do you want to update the titles of the clips? (yes/anything else): ")
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
            choice = input("Is '" + new_title + "' the title that you want? (yes/anything else): ")
            if choice != 'yes':
                new_title = input("Enter the new title: ")
            else:
                is_good = True
        
        clip.title = new_title
        print("'" + new_title + "' is the new title")

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

# Testing functions
def display_clips_test(clips):
    for clip in clips:
        print("==========")
        clip.display_clip_information()
        print("==========")

    return 0

def main():
    # Get user input clips
    clips = get_clips()
    display_clips_test(clips) # debugging

    # Handle titles
    include_titles = False
    title_duration = 0

    choice = input("Do you want to include titles of clips in the video (yes/anything else): ")
    if choice == 'yes':
        include_titles = True
        change_titles(clips)
    display_clips_test(clips) # debugging

    if include_titles:
        title_duration = get_duration()


if __name__ == '__main__':
    main()