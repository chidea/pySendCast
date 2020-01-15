from time import sleep
from logging import info, debug, warn, critical, error
from socket import socket
import struct
import sys

BCAST_PORT = 31023 # 31022 for sync_play
BCAST_MAGIC = 'ch.ideas_bcast.py'

class BroadCastSocket(socket):
  def __init__(self, port=None, magic=None):
    from socket import AF_INET, SOCK_DGRAM
    super().__init__(AF_INET, SOCK_DGRAM)#, IPPROTO_UDP
    super().setblocking(True)
    #super().setblocking(False)
    #super().settimeout(0)
    self.bcast_port = port or BCAST_PORT
    self.magic = (BCAST_MAGIC + (('_'+magic) if magic else '')).encode()
  
  def set_iface(self, iface):
    from sys import platform
    if platform == 'win32': return
    from socket import SOL_SOCKET, SO_BINDTODEVICE
    super().setsockopt(SOL_SOCKET, SO_BINDTODEVICE, iface.encode())

  def wait(self, num=0):
    pass

class BroadCastServSocket(BroadCastSocket):
  def __init__(self, port=None, magic=None):
    super().__init__(port, magic)
    from socket import AF_INET, SOL_SOCKET, SO_BROADCAST
    super().bind(('', 0))
    super().setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    super().settimeout(0)
    from sys import platform
    if platform == 'win32':
      from socket import inet_aton, getaddrinfo, gethostname
      addrs = getaddrinfo(gethostname(), 0, family=AF_INET)
      #ip = max(addrs, key=lambda v:int.from_bytes(inet_aton(v[-1][0]), 'big'))[-1][0]
      #self.bcast_addr = ip[:ip.rindex('.')+1]+'255'
      self.bcast_addrs = [v[:v.rindex('.')+1]+'255' for v in list(map(lambda v:v[-1][0], addrs))]
    else:
      self.bcast_addrs = ['<broadcast>']

  def send(self, data):
    #info('server sending : %s', data)
    try:
      #super().sendto(data, (self.bcast_addr, self.bcast_port))
      for addr in self.bcast_addrs:
        #print('server sending : %s to %s:%s', data, addr, self.bcast_port)
        super().sendto(data, (addr, self.bcast_port))
    except Exception as e:
      error('socket send error with : %s', e)

  def announce(self):
    self.send(self.magic)

  def announce_loop(self):
    try:
      while True:
        self.announce()
        sleep(1)
    except KeyboardInterrupt:
      print('finishing announce loop')

class BroadCastCliSocket(BroadCastSocket):
  def __init__(self, port=None, magic=None):
    super().__init__(port, magic)
    from socket import SOL_SOCKET, SO_REUSEADDR
    super().setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    self.serv_addr = []
    super().bind(('', self.bcast_port))

  def discovery(self):
    data, addr = super().recvfrom(len(self.magic)+2)
    #print('discovered message :', data)
    #print('discovered from :', addr)
    return None if data[:len(self.magic)] != self.magic else addr
    #if not addr in self.serv_addr:
    #  self.serv_addr.append(addr)
    #  print('added to server address :', addr)
  
  def send(self, data):
    if self.serv_addr is None: return
    super().sendto(data, self.serv_addr)

#def all_interfaces():
#  from array import array
#  from fcntl import ioctl
#  import socket
#  max_possible = 128 # arbitrary. raise if needed.
#  obytes = max_possible * 32
#  deb = b'\0'
#  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#  names = array('B', deb * obytes)
#  outbytes = struct.unpack('iL', ioctl(
#        s.fileno(),
#        0x8912,  # SIOCGIFCONF
#        struct.pack('iL', obytes, names.buffer_info()[0])
#        ))[0]
#
#  namestr = names.tostring()
#
#  lst = []
#  for i in range(0, outbytes, 40):
#    name = namestr[ i: i+16 ].split( deb, 1)[0]
#    name = name.decode()
#    #iface_name = namestr[ i : i+16 ].split( deb, 1 )[0]
#    ip = namestr[i+20:i+24]
#    lst.append((name, ip))
#    return lst

def test(is_serv):
  sock = (BroadCastServSocket if is_serv else BroadCastCliSocket)()
  try:
    if is_serv:
      sock.announce_loop()
    else:
      print('discovered :', sock.discovery())
  except KeyboardInterrupt:
    sock.close()

if __name__ == '__main__':
  from sys import argv
  is_serv = len(argv)>1 and argv[1]=='s'
  test(is_serv)#, '' if len(argv)<3 else argv[2]) #argv[2] if len(argv)>2 and argv[2] else '')
