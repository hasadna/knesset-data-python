# -*- coding: utf-8 -*-
import logging
import subprocess
import os
import xml.etree.ElementTree as ET
from .exceptions import AntiwordException
import six

# solve issues with unicode for python3/2
if six.PY2:
    def decode(a, b):
        return a
elif six.PY3:
    def decode(a, b):
        return a.decode(b)

logger = logging.getLogger(__name__)


def antixml(str):
    tree = ET.fromstring(str.replace("\n\n", ""))
    text = decode(ET.tostring(tree, encoding='utf8', method='text'), 'utf-8')
    text = "\n".join([line.strip() if len(line.strip()) == 0 else line for line in text.split("\n")])
    return text


def antiword(filename):
    if not os.path.exists(filename):
        raise IOError('File not found: %s'%filename)
    if os.environ.get('HOME', '') == '':
        # see http://stackoverflow.com/questions/11182095/antiword-doesnt-work-on-hosted-server
        os.environ.setdefault('ANTIWORDHOME', '/usr/share/antiword')
    cmd='LC_ALL=C LANG=C antiword -x db '+filename+' > '+filename+'.awdb.xml'
    try:
        logger.debug(cmd)
        output = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    except subprocess.CalledProcessError as e:
        raise AntiwordException(e.returncode, e.cmd, e.output)
    logger.debug(output)
    with open(filename+'.awdb.xml','r') as f:
        xmldata=f.read()
    logger.debug('len(xmldata) = '+str(len(xmldata)))
    os.remove(filename+'.awdb.xml')
    return xmldata


def fix_hyphens(text):
    return text.replace(u"\n\n–\n\n",u" – ")


def get_people_list(text,token):
    lines = text.split("\n")
    # find the start of the list
    start_index = 0
    end_index = 0
    found = False
    for i in range(len(lines)):
        
        if token in lines[i]:
            start_index = i
            found = True

        if (start_index > 0) and (i > start_index):
            if u":" in lines[i] :
                end_index = i
                break

    return list(filter(lambda x: x and (len(x) > 0), lines[start_index +1 : end_index-1]) if found else [])


def get_speaker_list(text, token=u'היו"ר'):
    fixed_text = fix_hyphens(text)
    lines = fixed_text.split("\n")
    start_index = 0
    found = False
    for i in range(len(lines)):
        start_index = i
        if token in lines[i] and ":" in lines[i]:
            found = True
            break
    if found:
        speakers = list(set(filter(lambda x: x and x[-1] == u':', lines[start_index:])))
        speakers = map(lambda x: x[:-1], speakers)
        speakers = filter(lambda x: u"קריאה" != x, speakers)
        speakers = filter(lambda x: u"קריאותנ" != x, speakers)

        return speakers

    return []
