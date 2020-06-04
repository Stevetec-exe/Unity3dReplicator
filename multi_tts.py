import gtts,pyttsx3

# wrapper for GTTS and pyttsx3, enables easy switching and more customization
def voice_renderer(text,filename,voice="GTTS_US"):
    ext = '.mp3'
    engine = pyttsx3.init()
    engine.setProperty('rate',145)

    voices = [v.id for v in engine.getProperty('voices')]
    if voice == 'GTTS_US':
        gtts.gTTS(text,lang="en-US").save(filename)
    elif voice == "GTTS_EN":
        gtts.gTTS(text,lang="en-GB").save(filename)
    elif voice in voices:
        ext = '.wav'
        engine.setProperty('voice', voice)  # changes the voice
        engine.save_to_file(text,filename+ext)
        engine.runAndWait()
    else:
        print('Invalid voice Setting "'+voice+'". Usable voices:\nGTTS_US\nGTTS_GB')
        print('\n'.join(voices))
    return filename+ext

def voice_say(text,voice):
    engine = pyttsx3.init()
    engine.setProperty('rate',145)

    voices = [v.id for v in engine.getProperty('voices')]
    if voice in voices:
        ext = '.wav'
        engine.setProperty('voice', voice)  # changes the voice
        engine.say(text)
        engine.runAndWait()
    else:
        print('Invalid voice Setting "'+voice+'". Usable voices:\nGTTS_US\nGTTS_GB')
        print('\n'.join(voices))