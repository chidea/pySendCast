import tarfile
from bcast import BroadCastCliSocket, BroadCastServSocket, BCAST_MAGIC
import socket
from os.path import basename
import glob

def mkpin(length=4):
  from random import choices
  from string import digits
  return ''.join(choices(digits, k=length))

if __name__ == '__main__':
  from sys import argv
  srv_addr = None
  if argv[1] in ('-up', '--userpin') and len(argv)>4:
    pin=argv[2]
    print('user PIN :', pin)
    argv = [argv[0]] + argv[3:]
  elif argv[1] in ('-p', '--pin'):
    pin=mkpin()
    print('generated PIN :', pin)
    argv = [argv[0]] + argv[2:]
  else: pin=''
  with BroadCastCliSocket(magic='sendfile'+pin) as s:
    try:
      while srv_addr is None:
        srv_addr = s.discovery()
      print('sending to :', (srv_addr[0], 18902))
    except KeyboardInterrupt:
      s.close()
  with socket.create_connection((srv_addr[0], 18902)) as s:
      with tarfile.open(fileobj=s.makefile('wb', buffering=0), mode='w|gz') as t:
        for a in argv[1:]:
          for f in glob.iglob(a):
            print('sending %s' %f)
            t.add(f, arcname=basename(f))
