import configparser  # read the .ini config

# Needed to fetch online resources
import requests
from io import BytesIO
from PIL import Image
import shutil

# Dispatch Systemcalls
import subprocess
import os

# Audio processing
from pydub import AudioSegment
# Extracting Wikipedia text
import wikipedia
# Used to filter invalid chars
import string

# wraps pyttsx3 and gtts in one simple function
from multi_tts import voice_renderer

# converts strings to it's auto-detected type. Only supports types needed in this tool
def toPyType(string):
    string = string.rstrip()
    if string.lower() in ["yes","true","y"]: out = True
    elif string.lower() in ["no","false","n"]: out = False
    else:
        try:
            out = int(string)
        except:
            out = string
    return out

# Function that loads and validates the config file
def validate_load_config():
    config = configparser.ConfigParser()  # initialize parser
    config.read('config.ini')  # read config file
    sections = config.sections()  # list all sections
    required = [  # required items, listing sections and their required variables
        ["ExternalDependencies",["Unity","Template"]],
        ["Features",["Build","Wikipedia","Music","Images"]],
        ["Images",["sizes"]],
        ["Music",["Loop","Voiceengine"]],
        ["Experimental",["offline","theme"]],
        ["Output",["Folder"]]]
    conf_dict = {}
    for req_section in required:  # loop over requirements
        if req_section[0] in config.sections():  # Section exists
            section = config[req_section[0]]  # extract section
            out = {}
            for req_var in req_section[1]:  # loop over required variables
                if req_var in section.keys():  # Variable exists
                    out[req_var] = section[req_var]  # add item to config dict
                else:  # variable missing
                    # raise human friendly error
                    raise ValueError(f"Section {req_section[0]} is missing the variable '{req_var}'")
            conf_dict[req_section[0]] = out

        else:  # section missing
            # raise human friendly error
            raise ValueError(f"Section {req_section[0]} is missing.")

    return conf_dict

# Downloads an image from unspash.com using the specified width/height/theme
def download_image(theme, filename,size_x,size_y):
    try:
        response = requests.get("https://source.unsplash.com/{}x{}/?".format(size_x,size_y)+theme)  # access the unsplash api
        img = Image.open(BytesIO(response.content))  # use BytesIO to save the image
        img.save(filename)
    except requests.exceptions.ConnectionError:
        raise ValueError("No internet connection, you need it to fetch images")

# Uses config values to run download_image as often as needed
def get_images(config,theme):  # theme as a second argument as it it is not included in the config
    for image_id,size in enumerate(config["Images"]["sizes"].split("/")):  # loop over the sizes
        destination = config["ExternalDependencies"]["Template"]+"\\background"+str(image_id)+".png"  # dest. file path
        if toPyType(config["Experimental"]["offline"]):  # when offline flag is set, let the user enter the file path to an image that will be used instead
            while True:
                try:
                    # try copy file from user supplied location to project destination
                    shutil.copy(input(f"[Offline mode] Image {image_id}, size {size}. Specify a file path:"),destination)
                    break  # no need to ask again, source and dest. valid
                except FileNotFoundError:  # user file doesn't exist, human friendly error message
                    print("The file you specified doesn't exist or this tool has no access to it.")
        else:  # download the images from the interwebz just as the prophecy foretold and they are in fact the images you are looking for
            download_image(theme,destination,size.split("x")[0],size.split("x")[1])

# creates 'custom' background track that
def get_music(config,theme):
    tts_filename = voice_renderer(theme,"TTS",voice=config["Music"]["Voiceengine"]) # create TTS file from theme
    base = AudioSegment.from_mp3(os.path.abspath(config["Music"]["Loop"]))  # load the base loop
    tts = AudioSegment.from_file(tts_filename)  # load the generated tts file
    tts += 10  # make tts louder
    tts_len = len(tts)  # get the tts length
    base_1 = base[0:tts_len]  # split the base at the timestamp the tts ends
    base_2 = base[tts_len+1:]  # cut the second part of the loop
    base_1 -= 10  # lower the volume of the first part
    base = base_1 + base_2  # concat the base loop back together
    backgroundTrack = base.overlay(tts)  # overlay the tts over the loop
    backgroundTrack.export(config["ExternalDependencies"]["Template"]+"\\BackgroundMusic.mp3", format="mp3")  # export the final product

# fetches the wikipedia article for a given theme.
def get_text(config,theme):
    # Fetch about text from wikipedia
    if toPyType(config["Experimental"]["offline"]):  # offline, let the user type something funny
        text = input("[Offline mode] Wikipedia replacement for '"+theme+"': ")
    else:
        text = wikipedia.summary(theme,sentences=3)  # fetch the summary [first part of article]
        #text = "code is working as expected if the text stays the same as there are no invalid or otherwise random chars here"
        # Remove any unprintable characters [Control chars etc.]
        # HACK / OPTIMIZE: This works but is in no way even remotely fast, there may well be a lib for that but the dependency list to high already.
        text = ''.join(c for c in text if c in string.printable)
    # save to file
    with open(config["ExternalDependencies"]["Template"]+"\\About.txt","w") as f:
        f.write(text)

# kicks off unity auto-build
def build_game(config,theme):
    theme = theme.replace(" ","_")  # repalce space with underscore to make it filepath-save
    # create the build command for the unity command line interface.
    # To use this, the project can't be opened in the Unity editor at the same time.
    build_command = "\""+config["ExternalDependencies"]["Unity"]+"""" -batchMode -quit -nographics"""
    build_command += """ -projectPath {}  -buildWindowsPlayer """.format(conf["ExternalDependencies"]["Template_root"])
    build_command += """{}\\{}\\{}.exe""".format(config["Output"]["Folder"],theme,theme+"_Game")
    subprocess.run(build_command)  # it's just as bad as os.system('evil code'), but the command has to be run somehow

if __name__ == '__main__':
    conf = validate_load_config()  # load the config
    # backup the project root
    conf["ExternalDependencies"]["Template_root"] = conf["ExternalDependencies"]["Template"]
    # remap the template to the projects 'Resources' folder
    conf["ExternalDependencies"]["Template"] = os.path.abspath(conf["ExternalDependencies"]["Template"]+"\\Assets\\Resources")

    if conf["Experimental"]["theme"].upper() == "STDIN":
        theme = input("Game theme: ")  # get the theme via STDIN
    else:
        theme = conf["Expreimental"]["theme"]  # take the theme from the config
    # Save game Name/Theme to file to be displayed as menu title
    with open(conf["ExternalDependencies"]["Template"]+"\\Gamename.txt","w") as f:
        f.write(theme)
    # Download images
    if toPyType(conf["Features"]["Images"]):
        print("--- Downloading Images ---")
        get_images(conf,theme)  # fetch images

    # Create background music
    if toPyType(conf["Features"]["Music"]):
        print("--- Creating Background Music ---")
        get_music(conf,theme)

    # Create About.txt
    if toPyType(conf["Features"]["Wikipedia"]):
        print("--- Fetching Wikipedia ---")
        get_text(conf,theme)

    if toPyType(conf["Features"]["Build"]):
        print("--- Building Game ---")
        build_game(conf,theme)
