# Uses the subreddit data to read in new posts for the given time period 

import sys

import src.AudioProcessor as _Audio
import src.ImageProcessor as _Images
import src.RedditProcessor as _Reddit
import src.VideoProcessor as _Videos
import src.CmdProcessor as _Cmd
import src.TxtProcessor as _Txt

_Cmd.verify( sys.argv, 2, 'please provide url')

def run ( url, outname ) :

    print( 'starting scrape . . .')
    post = _Reddit.get_submission( url )

    print( 'reading data from scrape . . .')
    post_data = _Reddit.get_commentStreams( post )

    print( 'formating and cleaning data . . . ')
    serialized_post_data = _Reddit.get_serializedStreams( post_data, 500) 

    print( 'generating audio . . .' )
    audio_generated = _Audio.get_processedStream( serialized_post_data, False )

    print( 'generating images . . .' )
    image_generated = _Images.get_processedStream( serialized_post_data, False )

    print ( 'generating video . . .')
    _Videos.combine( audio_generated, outname )

# Determine way to run code
if ( sys.argv[1] == 'txt' ) :
    data = _Txt.get_readList()
    [ run ( name, str(i) ) for i,name in enumerate( data )  ]
else:
    run ( sys.argv[1], 'output' )
