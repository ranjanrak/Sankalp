import re
import sys
import six

def byte_adaptor(fbuffer):
        strings = fbuffer.read().decode('latin-1')
        fbuffer = six.StringIO(strings)
        return fbuffer


def js_adaptor(buffer):
    buffer = re.sub('true', 'True', buffer)
    buffer = re.sub('false', 'False', buffer)
    buffer = re.sub('none', 'None', buffer)
    buffer = re.sub('NaN', '"NaN"', buffer)
    return buffer