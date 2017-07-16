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
