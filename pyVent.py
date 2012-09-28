"""
Python Ventrilo Status
by Philip Davies
 -- Derived from work by Luigi Auriemma

INTRODUCTION
============
This algorithm is the method used by the chat program Ventrilo
(http://www.ventrilo.com) for encoding the UDP packets used to get
the status informations.

LICENSE
=======
    Copyright 2007 Philip Davies
    Copyright 2005,2006 Luigi Auriemma

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

    http://www.gnu.org/licenses/gpl.txt


=======

    If you modify or create derivative works based on this code, please respect
    our work and carry along our Copyright notices along with the GNU GPL.
    The GPL DOES NOT allow you to release modified or derivative works under
    any other license. Before you modify this code, read up on your rights
    and obligations under the GPL.

"""
from struct import *

VENT_HEADSIZE = 20
VENT_MAXPACKETSIZE = 512
VENT_MAXPACKETCOUNT = 32

VENT_UDP_ENCDATA_HEAD = [
  0x80, 0xe5, 0x0e, 0x38, 0xba, 0x63, 0x4c, 0x99, 0x88, 0x63, 0x4c, 0xd6, 0x54, 0xb8, 0x65, 0x7e,
  0xbf, 0x8a, 0xf0, 0x17, 0x8a, 0xaa, 0x4d, 0x0f, 0xb7, 0x23, 0x27, 0xf6, 0xeb, 0x12, 0xf8, 0xea,
  0x17, 0xb7, 0xcf, 0x52, 0x57, 0xcb, 0x51, 0xcf, 0x1b, 0x14, 0xfd, 0x6f, 0x84, 0x38, 0xb5, 0x24, 
  0x11, 0xcf, 0x7a, 0x75, 0x7a, 0xbb, 0x78, 0x74, 0xdc, 0xbc, 0x42, 0xf0, 0x17, 0x3f, 0x5e, 0xeb,
  0x74, 0x77, 0x04, 0x4e, 0x8c, 0xaf, 0x23, 0xdc, 0x65, 0xdf, 0xa5, 0x65, 0xdd, 0x7d, 0xf4, 0x3c,
  0x4c, 0x95, 0xbd, 0xeb, 0x65, 0x1c, 0xf4, 0x24, 0x5d, 0x82, 0x18, 0xfb, 0x50, 0x86, 0xb8, 0x53,
  0xe0, 0x4e, 0x36, 0x96, 0x1f, 0xb7, 0xcb, 0xaa, 0xaf, 0xea, 0xcb, 0x20, 0x27, 0x30, 0x2a, 0xae,
  0xb9, 0x07, 0x40, 0xdf, 0x12, 0x75, 0xc9, 0x09, 0x82, 0x9c, 0x30, 0x80, 0x5d, 0x8f, 0x0d, 0x09,
  0xa1, 0x64, 0xec, 0x91, 0xd8, 0x8a, 0x50, 0x1f, 0x40, 0x5d, 0xf7, 0x08, 0x2a, 0xf8, 0x60, 0x62,
  0xa0, 0x4a, 0x8b, 0xba, 0x4a, 0x6d, 0x00, 0x0a, 0x93, 0x32, 0x12, 0xe5, 0x07, 0x01, 0x65, 0xf5,
  0xff, 0xe0, 0xae, 0xa7, 0x81, 0xd1, 0xba, 0x25, 0x62, 0x61, 0xb2, 0x85, 0xad, 0x7e, 0x9d, 0x3f,
  0x49, 0x89, 0x26, 0xe5, 0xd5, 0xac, 0x9f, 0x0e, 0xd7, 0x6e, 0x47, 0x94, 0x16, 0x84, 0xc8, 0xff,
  0x44, 0xea, 0x04, 0x40, 0xe0, 0x33, 0x11, 0xa3, 0x5b, 0x1e, 0x82, 0xff, 0x7a, 0x69, 0xe9, 0x2f,
  0xfb, 0xea, 0x9a, 0xc6, 0x7b, 0xdb, 0xb1, 0xff, 0x97, 0x76, 0x56, 0xf3, 0x52, 0xc2, 0x3f, 0x0f,
  0xb6, 0xac, 0x77, 0xc4, 0xbf, 0x59, 0x5e, 0x80, 0x74, 0xbb, 0xf2, 0xde, 0x57, 0x62, 0x4c, 0x1a,
  0xff, 0x95, 0x6d, 0xc7, 0x04, 0xa2, 0x3b, 0xc4, 0x1b, 0x72, 0xc7, 0x6c, 0x82, 0x60, 0xd1, 0x0d]

VENT_UDP_ENCDATA_DATA = [
  0x82, 0x8b, 0x7f, 0x68, 0x90, 0xe0, 0x44, 0x09, 0x19, 0x3b, 0x8e, 0x5f, 0xc2, 0x82, 0x38, 0x23,
  0x6d, 0xdb, 0x62, 0x49, 0x52, 0x6e, 0x21, 0xdf, 0x51, 0x6c, 0x76, 0x37, 0x86, 0x50, 0x7d, 0x48,
  0x1f, 0x65, 0xe7, 0x52, 0x6a, 0x88, 0xaa, 0xc1, 0x32, 0x2f, 0xf7, 0x54, 0x4c, 0xaa, 0x6d, 0x7e,
  0x6d, 0xa9, 0x8c, 0x0d, 0x3f, 0xff, 0x6c, 0x09, 0xb3, 0xa5, 0xaf, 0xdf, 0x98, 0x02, 0xb4, 0xbe,
  0x6d, 0x69, 0x0d, 0x42, 0x73, 0xe4, 0x34, 0x50, 0x07, 0x30, 0x79, 0x41, 0x2f, 0x08, 0x3f, 0x42,
  0x73, 0xa7, 0x68, 0xfa, 0xee, 0x88, 0x0e, 0x6e, 0xa4, 0x70, 0x74, 0x22, 0x16, 0xae, 0x3c, 0x81,
  0x14, 0xa1, 0xda, 0x7f, 0xd3, 0x7c, 0x48, 0x7d, 0x3f, 0x46, 0xfb, 0x6d, 0x92, 0x25, 0x17, 0x36,
  0x26, 0xdb, 0xdf, 0x5a, 0x87, 0x91, 0x6f, 0xd6, 0xcd, 0xd4, 0xad, 0x4a, 0x29, 0xdd, 0x7d, 0x59,
  0xbd, 0x15, 0x34, 0x53, 0xb1, 0xd8, 0x50, 0x11, 0x83, 0x79, 0x66, 0x21, 0x9e, 0x87, 0x5b, 0x24,
  0x2f, 0x4f, 0xd7, 0x73, 0x34, 0xa2, 0xf7, 0x09, 0xd5, 0xd9, 0x42, 0x9d, 0xf8, 0x15, 0xdf, 0x0e,
  0x10, 0xcc, 0x05, 0x04, 0x35, 0x81, 0xb2, 0xd5, 0x7a, 0xd2, 0xa0, 0xa5, 0x7b, 0xb8, 0x75, 0xd2,
  0x35, 0x0b, 0x39, 0x8f, 0x1b, 0x44, 0x0e, 0xce, 0x66, 0x87, 0x1b, 0x64, 0xac, 0xe1, 0xca, 0x67,
  0xb4, 0xce, 0x33, 0xdb, 0x89, 0xfe, 0xd8, 0x8e, 0xcd, 0x58, 0x92, 0x41, 0x50, 0x40, 0xcb, 0x08,
  0xe1, 0x15, 0xee, 0xf4, 0x64, 0xfe, 0x1c, 0xee, 0x25, 0xe7, 0x21, 0xe6, 0x6c, 0xc6, 0xa6, 0x2e,
  0x52, 0x23, 0xa7, 0x20, 0xd2, 0xd7, 0x28, 0x07, 0x23, 0x14, 0x24, 0x3d, 0x45, 0xa5, 0xc7, 0x90,
  0xdb, 0x77, 0xdd, 0xea, 0x38, 0x59, 0x89, 0x32, 0xbc, 0x00, 0x3a, 0x6d, 0x61, 0x4e, 0xdb, 0x29]
  
VENT_CRCDATA = [
  0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
  0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
  0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
  0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
  0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
  0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
  0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
  0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
  0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
  0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
  0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,
  0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
  0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
  0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
  0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
  0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
  0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
  0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
  0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
  0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
  0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
  0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
  0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
  0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
  0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
  0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,
  0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
  0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,
  0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
  0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
  0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
  0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0]

class VentPacket:
  header_keys = ['key','zero','cmd','id','totlen','len','totpck','pck','datakey','crc']
  header_items = dict([(i,0) for i in range(10)])
  packet = ''.join([chr(0) for i in range(20)])
  def __getattr__(self,name):
    if name in self.header_keys:
      return self.header_items[self.header_keys.index(name)]
    elif name == "header":
      return self.packet[:20]
    elif name == "data":
      return self.packet[20:]
    raise AttributeError, name  # <<< DON'T FORGET THIS LINE !!
  def __setattr__(self,name,value):
    if name == "packet" and ( len(value) < VENT_HEADSIZE or len(value) > VENT_MAXPACKETSIZE):
        raise Exception, "Packet length must be between %s and %s."%(VENT_HEADSIZE,VENT_MAXPACKETSIZE)
    if name in self.header_keys:
      self.header_items[self.header_keys.index(name)] = value
    elif name == "header":
      if len(value)!=20:
        raise Exception, "Header must be 20 bytes in length"
      else:
        self.__dict__["packet"] = value + self.data
    elif name == "data":
      self.__dict__["packet"] = self.header + value
    else:
      self.__dict__[name] = value
  def calcCRC(self,data=None,dont_set=False):
    if not data: data = self.rawdata
    crc = 0
    for c in data:
      crc = VENT_CRCDATA[crc >> 8] ^ ord(c) ^ (crc << 8)
    if not dont_set: self.crc = crc
    else: return crc 
  def createKeys(self,is_head = False,key=None):
    from random import randint
    if not key:
      key = unpack("<H",pack("@H", randint(1,65536) ))[0] & 0x7fff
    a1 = key % 2**8
    if a1 == 0: raise Exception, "ERROR: Invalid Key"
    a2 = key >> 8
    if a2 == 0:
      a2 = is_head and 69 or 1
      key = key | (a2 << 8)
    return key,a1,a2
    

class VentRequestPacket(VentPacket):
  def encodeHeader(self):
    self.key,a1,a2 = self.createKeys(True)
    enchead = pack("!H",self.key)
    chars  = [i for i in ''.join([pack("!H",self.header_items[i]) for i in range(1,len(self.header_items))])]
    for i in range(len(chars)):
      enchead = enchead + chr((ord(chars[i]) + VENT_UDP_ENCDATA_HEAD[a2] + (i % 5)) % 2**8)
      a2 = (a2 + a1) % 2**8
    self.header = enchead
  def encodeData(self):
    self.datakey,a1,a2 = self.createKeys(False)
    encdata = ''
    chars = [i for i in self.rawdata]
    for i in range(len(chars)):
      encdata = encdata + chr((ord(chars[i]) + VENT_UDP_ENCDATA_DATA[a2] + (i % 72)) % 2**8)
      a2 = (a2 + a1) % 2**8
    self.data = encdata
  def __init__(self,cmd=None,id=None,password=""):
    self.rawdata = pack("16s",password)
    self.zero = 0
    self.cmd = cmd in [1,2,7] and cmd or 1
    self.id = id
    self.totlen = len(self.rawdata)
    self.len = self.totlen
    self.totpck = 1
    self.pck = 0
    self.calcCRC();
    self.encodeData();
    self.encodeHeader();
    
    
class VentResponsePacket(VentPacket):
  def __init__(self,packet):
    self.packet = packet
    self.decodeHeader()
    self.decodeData()
  def decodeHeader(self):
    key = unpack("!10H",self.header)[0]
    _,a1,a2 = self.createKeys(True,key)
    decoded = ''
    for i in range(18):
      decoded = decoded + chr((ord(self.header[i+2]) - VENT_UDP_ENCDATA_HEAD[a2] - (i % 5)) % 2**8)
      a2 = (a2 + a1) % 2**8
    index = 1
    for i in unpack("!9H",decoded):
      self.header_items[index] = i
      index = index + 1
  def decodeData(self):
    _,a1,a2 = self.createKeys(False,self.datakey)
    decdata = ''
    chars = [i for i in self.data]
    for i in range(len(chars)):
      val = (ord(chars[i]) - VENT_UDP_ENCDATA_DATA[a2] - (i % 72)) % 2**8
      decdata = decdata + chr(val)
      a2 = (a2 + a1) % 2**8
    self.rawdata = decdata

class VentriloServer:
  valid_cmds = [1,2,7]
  
  def __init__(self,host,port=None,password=None):
    if type(host)==tuple:
      self.ip = host[0]
      self.port = host[1] or 3784
    else:
      self.ip = host
      self.port = 3784
    self.password = password or ""
    
  def connect(self):
    import socket
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    self.socket.connect((self.ip,self.port))
    self.socket.settimeout(1)
    
  def request(self,cmd):
    from time import time
    if not getattr(self,'socket',None): self.connect()
    id = int(time())%2**16
    packets,response = {},""
    r = VentRequestPacket(cmd,id,self.password)
    if len(r.packet)!= self.socket.send(r.packet):
      raise Exception, "Not all data sent"
    while(True):
      rawpacket = self.socket.recv(VENT_MAXPACKETSIZE)
      if not rawpacket: break
      p = VentResponsePacket(rawpacket)
      if p.id != id: raise Exception, "Response not from the previous request"
      if not p.pck in packets: packets[p.pck] = p
      if len(packets) == p.totpck: break
    for i in range(len(packets)):
      response = response + packets[i].rawdata
    self.last_response, self.last_packets = response,packets
    return response,packets

  def _split(self,line):
    return int(line[:2]),line[2:]
  def parseStatusResponse(self,line):
    s = self.getStatus()
    cmd,value = self._split(line)
    if cmd ==  0: s['name'] = value
    if cmd ==  1: s['phonetic'] = value
    if cmd ==  2: s['comment'] = value
    if cmd ==  3: s['auth'] = int(value)
    if cmd ==  4: s['maxclients'] = int(value)
    if cmd ==  5: s['voicecodec'] = value
    if cmd ==  6: s['voiceformat'] = value
    if cmd ==  7: s['uptime'] = int(value)
    if cmd ==  8: s['platform'] = value
    if cmd ==  9: s['version'] = value
    if cmd == 10: s['channelcount'] = int(value)
    if cmd == 11: self.addChannel(value)
    if cmd == 12: s['usercount'] = int(value)
    if cmd == 13: self.addUser(value)
    
  def updateStatus(self):
    s = self.getStatus()
    for i in [x for x in s]: del s[i]
    response,_ = self.request(7)
    for line in response.split('\n'):
      if line=="\x00": break
      self.parseStatusResponse(line)
  
  def printResponse(self,cmd):
    if cmd not in self.valid_cmds:
      raise Exception, "Invalid command (%s) requested. Must be in %s"%(cmd,self.valid_cmds.__repr__())
    self.request(cmd)
    print self.last_response

  def addUser(self,data):
    user = {}
    for item in data.split(","):
      cmd,value = self._split(item)
      if   cmd == 0: user['id'] = int(value)
      elif cmd == 1: user['admin'] = value=='1'
      elif cmd == 2: user['channel'] = int(value)
      elif cmd == 3: pass # PHAN?
      elif cmd == 4: user['ping'] = int(value)
      elif cmd == 5: user['time'] = int(value)
      elif cmd == 6: user['name'] = value
      elif cmd == 7: user['comment'] = value
    self.getUsers().append(user)
    
  def addChannel(self,data):
    channel = {}
    for item in data.split(","):
      cmd,value = self._split(item)
      if   cmd == 0: channel['id'] = int(value)
      elif cmd == 1: pass # PID?
      elif cmd == 2: channel['protected'] = value=='1'
      elif cmd == 3: channel['name'] = value
      elif cmd == 4: channel['comment'] = value
    self.getChannels().append(channel)
      
  def getStatus(self):
    if not getattr(self,'status',None): self.status = {}
    return self.status
  
  def getUsers(self):
    s = self.getStatus()
    if not 'users' in s:
      s['users'] = []
    return s['users']
    
  def getChannels(self):
    s = self.getStatus()
    if not 'channels' in s:
      s['channels'] = []
    return s['channels']

  def getChannelUsers(self,channel):
    return [u for u in self.getUsers() if u['channel'] == channel]

  def getChannelById(self,channel):
    for chan in self.getChannels():
      if chan['id'] == channel:
        return chan

  def getTime(self,seconds):
    return ":".join([v<10 and "0"+str(v) or str(v) for v in (seconds / 3600, (seconds % 3600) / 60, seconds % 60)])

  def printStatus(self):
    def reprUser(user):
      return "%s %s[%sms, %s]"%(user['name'],user['comment'] and "(%s) "%user['comment'] or "",user['ping'],self.getTime(user['time']))
    self.updateStatus()
    status = self.getStatus()
    users = self.getChannelUsers(0)
    print status['name']
    for user in users:
      print reprUser(user)
    self.getChannels().sort(cmp=lambda x,y: cmp(x['name'],y['name']))
    for chan in self.getChannels():
      users = self.getChannelUsers(chan['id'])
      print len(users) and "+" or "-", chan['name']
      for user in users:
        print " %s"%reprUser(user)
        
"""
Usage Example:
--------------

>>> v = VentriloServer((ip,port),password)
>>> v.updateStatus()
>>> v.getStatus()
{'comment': '', 'uptime': 2217430, 'name': 'Plug', 'platform': 'WIN32', 'channelcount': 2, 'auth': 1, 'channels': [{'comment': '', 'protected': False, 'id': 2, 'name': 'The Boardroom'}, {'comment': '', 'protected': False, 'id': 246, 'name': 'LIKE ARENA K'}], 'voiceformat': '1,11 KHz%2C 16 bit', 'version': '2.3.1', 'maxclients': 20, 'phonetic': 'Plug', 'users': [{'comment': '', 'name': 'Maoli', 'admin': False, 'ping': 141, 'time': 81036, 'id': 242, 'channel': 2}, {'comment': '', 'name': 'Karnicus', 'admin': False, 'ping': 15, 'time': 38939, 'id': 254, 'channel': 2}], 'voicecodec': '0,GSM 6.10', 'usercount': 2}
>>> v.printStatus()
Plug
- LIKE ARENA K
+ The Boardroom
 Maoli [141ms, 22:31:16]
 Karnicus [15ms, 10:49:39]
>>> for chan in v.getChannels():
  print "%s [%s]"%(chan['name'],','.join([u['name'] for u in v.getChannelUsers(chan['id'])]))
"""



  
  
  
  
