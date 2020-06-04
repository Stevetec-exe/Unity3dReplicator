# Unity3dReplicator
Inspired by this GDC talk: ["1,500 Slot Machines Walk into a Bar: Adventures in Quantity Over Quality"](https://www.youtube.com/watch?v=E8Lhqri8tZk)
This tool reskins a Unity3d project by replacing images, audio and text files used as background or other customizable aspects.

# Features
* Replace images of any size and amount with stock images
* Generate a simple background loop based on the game theme
* Fetch the summary of the Wikipedia article about the theme
* Auto-build the game after customization
* Settings and control flow in one .ini file

# Project structure/ File reference

### Reskin.py [Main file]
This is the main part of this tool, it contains all customization stages and execution flow.

### Config.ini [main config]
Contains the generation settings and controlles
* what customization/build stage gets run
* path to required base files and Output directory
* Stage specific data

### multi_tts.py [python dependency]
A module that makes TextToSpeech simple by wrapping gtts and pyttsx into one reusable, simple to understand function

# Example project
To stay below the Github upload limit of 100mb I had to host the Project on a different service,
you can get it from my website: https://stevetec.de/downloads/UnityProject.zip
It's a simple 3D flappy bird clone. The game is not up to the highest code/design standards
[it's only supposed to be an example of the unity side of the customizer]
