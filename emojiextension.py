from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

from pkg_resources import resource_stream, resource_listdir

import json
import io
import os
import codecs

EMOJI_RE = r'(::)(.*?)::'

class EmojiExtension(Extension):

    def __init__(self, **kwargs):
        super(EmojiExtension, self).__init__(**kwargs)
                
    def extendMarkdown(self, md, md_globals):
        # Read the Emojis from the Resource:
        emoji_list = json.loads(resource_stream('resources', 'emojis.json').read().decode('utf-8'))
        # Turn the Emojis into a Dictionary for faster lookups:
        emojis = dict((emoji['key'], emoji['value']) for emoji in emoji_list)
        # And add the EmojiInlineProcessor to the Markdown Pipeline:
        md.inlinePatterns.add('emoji', EmojiInlineProcessor(EMOJI_RE, emojis) ,'<not_strong')
        
class EmojiInlineProcessor(Pattern):
    
    def __init__(self, pattern, emojis):
        super(EmojiInlineProcessor, self).__init__(pattern)
        
        self.emojis = emojis
        
    def handleMatch(self, m):
        emoji_key = m.group(3)
        
        return self.emojis.get(emoji_key, '')