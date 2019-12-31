from moviepy.editor import *

import os

path = os.path.dirname(os.path.abspath(__file__))

audioDir = os.path.join( path, '..', 'out', 'tmp', 'audio' )
imageDir = os.path.join( path, '..', 'out', 'tmp', 'images' )
transition_path = os.path.join( path, '..', 'assets', 'transition.gif' )
final_output = os.path.join( path, '..', 'out', 'videos', '[].mp4')


def formClip ( id ):

    audio = os.path.join( audioDir, str(id) + '.mp3' )
    img = os.path.join( imageDir, str(id) + '.png' )

    audio = AudioFileClip( audio )
    img = ImageClip( img ).set_duration( audio.duration )

    return img.set_audio( audio )

def combine ( data, out ):

    title, streams = data

    search_id = 0
    transition = VideoFileClip( transition_path ).set_duration( 0.75 )

    clips = [ ]

    for stream in streams :
        for comment in stream:
            for phrase in comment :
                search_id += 1
                clips.append( formClip( search_id ) )
        
        clips.append( transition )

    title_clips = [ formClip( search_id + i + 1 ) for i,p in enumerate(title) ]
    title_clips.append( transition )
    title_clips.extend ( clips )
    

    final = concatenate_videoclips ( title_clips )
    final_sped = final.speedx(factor=1.3)
    final.write_videofile( final_output.replace('[]', out), fps = 24 )
        
    print ( 'cleaning filed . . .')

    for filename in os.listdir(audioDir):
        os.unlink( os.path.join( audioDir, filename) )
    for filename in os.listdir(imageDir):
        os.unlink( os.path.join( imageDir, filename) )