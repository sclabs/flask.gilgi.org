import urllib
import xml.etree.ElementTree as ET
import steamdata
import json

def getdata():
    try:
        members = getmembers()
        if members == None:
            return None
        data = urllib.urlopen(steamdata.dataurl + ",".join(members))
        return json.load(data)
    except:
        return None

def getmembers():
    try:
        xml = urllib.urlopen(steamdata.memberslisturl)
        tree = ET.parse(xml)
        root = tree.getroot()
        members = []
        for member in root.iter('steamID64'):
            members.append(member.text)
        return members
    except:
        return None
