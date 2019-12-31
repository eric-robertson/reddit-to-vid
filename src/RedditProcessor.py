import re
import praw

reddit = praw.Reddit(client_id='nTIIjYwrfp4bSg', client_secret='2L-8nnubMNY6L28ykvfyESkJ3M4', user_agent='UghBot')

def get_submission ( url ):
    return reddit.submission(url=url)

def get_commentStreams ( submission ) :

    submission.comments.replace_more(limit=0)

    # Takes in content and cleans it up
    def cleanContent ( txt ) :
        linksStripped = re.sub(r'\[(.*)\][^\s]*', r'\1', txt)
        urlsStripped = re.sub(r'http[^\s]*', r'', linksStripped)
        cleaned = urlsStripped.encode('ascii', 'ignore').decode('ascii')
        return cleaned

    # Recursively extracts comment chains
    def extractComments ( body, source ) :

        chain = [ body ]
        while len( source.replies ) != 0 and len( chain ) < 5:

            #Comment must have 10% of their parents votes
            if ( source.replies[0].score / source.score  < 0.1 ) : break

            #Comments must have 100 votes
            if ( source.replies[0].score < 100 ): break

            chain.append( cleanContent( source.replies[0].body ) )
            source = source.replies [0] 

        return chain

    commentFeeds = []

    # For a top level comment to be chosen
    for top_level_comment in submission.comments:

        # Remove urls and clean text
        body = cleanContent ( top_level_comment.body )

        # Must have atleast 200 points
        if ( top_level_comment.score < 200 ): continue

        # Attempts to filter out 'list' like posts
        if ( len(body) / len( body.split('\n') ) < 80 ) : continue

        commentFeeds.append( extractComments ( body, top_level_comment ) )

    return ( submission.title, commentFeeds )

def get_serializedStreams ( commentStreams, target_phrases ):

    cuttoff = 250
    last = ''

    while True :
        phrases, data = try_serializedStreams ( commentStreams, cuttoff)
        if ( phrases > target_phrases ):
            cuttoff += 25
            if ( last == 'down' ):
                return data
            last = 'up'
        else:
            cuttoff -= 25
            if ( cuttoff < 0 ):
                return data
            if ( last == 'up'):
                return data
            last = 'down'

def try_serializedStreams ( commentStreams, cuttoff ):

    title, streams = commentStreams
    output = []

    streams_num = 0
    comments_num = 0
    phrases_num = 0

    def serialize ( i ) :
        split = re.split( r'([\.,:;!?\n])', i )
        joined = [ split[i] + split[i+1] for i in range( len( split ) - 1 ) if i % 2 == 0 ]    
        joined.append( split [-1] )
        return joined
        
    for stream in streams :

        size = 0
        _phrases = 0

        serialized_stream = []
        
        for comment in stream :

            phrases = serialize(comment)
            serialized_stream.append( phrases )

            size += len ( comment )
            _phrases += len( phrases )
            
        if ( size > cuttoff ):
            output.append( serialized_stream )
            streams_num += 1
            comments_num += len( stream )
            phrases_num += _phrases

    return ( phrases_num, ( serialize( title ), output ))
