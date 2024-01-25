
import urllib.parse as urllib_parse

# double encode problem with vercel
class StringConverter:
    regex = "[a-zA-Z0-9 %]+"
    
    def to_python(self, value):
        print("to_python", value)
        return urllib_parse.unquote(urllib_parse.unquote(value))
    
    def to_url(self, value):
        print("to_url", value)
        return value