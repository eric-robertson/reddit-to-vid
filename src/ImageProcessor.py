
from PIL import Image, ImageDraw, ImageFont
import os

path = os.path.dirname(os.path.abspath(__file__))
fontpath = os.path.join( path, '..','assets', 'Roboto-Bold.ttf' )

nsfwpath = os.path.join( path, '..', 'assets', 'nsfw.jpg' )
spacepath = os.path.join( path, '..', 'assets', 'space.jpg' )
scorepath = os.path.join( path, '..', 'assets', 'score.PNG' )
outputPath = os.path.join( path, '..', 'out', 'tmp', 'images')
font = ImageFont.truetype( fontpath, size=30 )
titleFont = ImageFont.truetype( fontpath, size=80 )

img_id = 0

def get_background ( is_nsfw ):
    if is_nsfw : 
        return Image.open(nsfwpath)
    return Image.open(spacepath)
def get_blank ( ):
    return Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))

def get_size ( text, f = font ):
    x,y = f.getsize(text)
    return x

def get_processedStream ( stream, is_nsfw ) :

    global img_id
    title, streams = stream
    output = [] 

    for commentChain in streams :

        processed = get_processedCommentChain ( commentChain )
        output.append( generate_images ( processed, is_nsfw ) )
    

    processed_title = get_processedCommentChain ( [ title ], titleFont, 3)
    
    title = generate_images ( processed_title, is_nsfw, titleFont, 2 )
    img_id = 0
    return ( title, output )

def get_processedCommentChain ( chain, f = font, s = 1 ):

    # constants for layout
    x,y = 0,0
    comment_gap = 30
    line_gap = 40 * s
    screen_end = 1800
    indent = 0
    indent_size = 80
    word_space = 20 * s
    heights  = []

    output = []

    for comment in chain :

        y += comment_gap

        # breaks a phrase into individual words with x and y positions
        for phrase in comment :

            if( len(phrase) == 0 ): continue

            phrase_peices = [ ]
            words = phrase.split(' ')

            x-= word_space

            for word in words:
                size = get_size ( word, f)
            
                x += word_space

                if word == '\n':
                    y += line_gap
                    x = indent

                elif x + size < screen_end:
                    phrase_peices.append( (x,y,word) )
                    x += size
                else:
                    y += line_gap
                    x = indent
                    phrase_peices.append( (x,y,word) )
                    x += size

            output.append( phrase_peices )
    
            if ( y >= 900 ):
                heights.append( y )
                y = 0
                x = 0
                output[-1].append( (-2,-2,'') )

        output[-1].append( (-1,-1,'') )
        y += line_gap

        if ( y >= 700 and x!=0 ):
            heights.append( y )
            y = 0
            x = 0
            output[-1].append( (-2,-2,'') )

        indent += indent_size
        x = indent
    
    heights.append( y )
    return (heights, output)

def generate_images ( chain, is_nsfw, f = font, s = 1 ) :
    
    heights, processed_chain = chain

    global img_id

    offset = ( 1080 - heights[0] ) // 2
    heights = heights[1:]
    img = get_background( is_nsfw )
    draw = ImageDraw.Draw(img, 'RGBA')
    output = []

    score = Image.open(scorepath, 'r')
    icon = True
    clear = False

    for phrase in processed_chain :

        for peice in phrase :

            x,y,word = peice
            X,Y = x + 100,y + offset - 50

            if ( x == -1 ) :
                icon = True
                continue

            if ( y == -2 ):
                clear = True
                continue

            if ( word == ' ' or len( word) == 0): continue
            
            if ( icon and s == 1 ):
                img.paste( score, (X-70,Y-3) )
                icon = False

            draw.rectangle( [X - 5 * ( s*s*s) ,Y-(3 * s * s ),X+get_size(word, f)+ (17 *s) ,Y+(60 * s)], fill=(26,26,26))
            draw.text((X,Y), word, font = f, align ="left")  

        img_id += 1
        output_path = os.path.join( outputPath, str(img_id) + '.png')
        img.save(output_path, 'PNG')
        output.append( img_id )

        if clear :
            offset = ( 1080 - heights[0] ) // 2
            heights = heights[1:]
            img = get_background( is_nsfw )
            draw = ImageDraw.Draw(img, 'RGBA')
            clear = False

    return output


        