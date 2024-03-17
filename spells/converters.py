
import urllib.parse as urllib_parse

# double encode problem with vercel
class StringConverter:
    """Personal string convertor to convert stuff like %20 to ' '"""

    regex = "[a-zA-Z0-9 %]+"
    
    def to_python(self, value):
        prev_value, value = value, urllib_parse.unquote(value)
        while prev_value != value:
            prev_value, value = value, urllib_parse.unquote(value)
        return value
    
    def to_url(self, value):
        return value