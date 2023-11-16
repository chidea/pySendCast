import tarfile
from .bcast import BroadCastServSocket,BroadCastCliSocket, BCAST_MAGIC
import socket
import timeit
from threading import Thread

def openurl(url):
  import webbrowser
  try:
    if webbrowser.get():
      webbrowser.open(url)
  except webbrowser.Error:
    from shutil import which
    if which('termux-open-url'):
      from os import system
      system('termux-open-url '+url)

def extract_all(tar):
  from .send import isurl
  #mems = tar.getmembers()
  #print('length of tar members : ', len(mems))
  for m in tar:
    if m.size == 0:
      if isurl(m.name):
        openurl(m.name)
      else: # simple message
        print(m.name)
      continue
    extract(m, tar)
  
def extract(f, tar):
  print('extracting %s (%d bytes)'%(f.name,f.size))
  timeit.gc.disable() 
  t0=timeit.default_timer()
  tar.extract(f, filter='data')
  #read = tar.extractfile(f)
  t0=timeit.default_timer()-t0
  timeit.gc.enable()
  print(f'extracting {f.name} done ({f.size} bytes, {t0} seconds, {f.size/t0/10**6} MB/s)')
  
def main(argv):
  if len(argv)>1 and argv[1]:
    if argv[1] in ('n', 'new', 'g', 'gen'):
      from .send import mkpin
      pin = mkpin()
      print('generated PIN :', pin)
    else: pin = argv[1]
  else: pin = ''
    
  sockets = []
  threads = []
  with socket.socket() as s:
    s.bind(('', 18902))
    s.setblocking(True)
    s.settimeout(1)
    s.listen()
    try:
      while True:
        with BroadCastServSocket(magic='sendfile'+pin) as sa:
          print('announcing')
          sa.announce()
        try:
          c, a = s.accept()
          print('receiving from : ', a[0]) # ip address
          fo = c.makefile('rb', buffering=0)
          tar = tarfile.open(fileobj=fo, mode='r|gz')
          
          t = Thread(target=extract_all, args=[tar])
          t.run()
          sockets.append(sa)
          threads.append(t)
          break
          
          #from .send import isurl
          #with tarfile.open(fileobj=fo, mode='r|gz') as tar:
          #  for f in tar:
          #    if f.size == 0:
          #      if isurl(f.name):
          #        openurl(f.name)
          #      else: # plain message
          #        print(f.name)
          #      continue
              #t = Thread(target=extract, args=[f, tar])
              #t.run()
              #threads.append(t)
            #s.close()
            #break # complete -> break loop 
        except socket.timeout:
          continue
    except KeyboardInterrupt:
      s.close()
      print('user canceled receiving')
      return 1
  for t in threads:
    t.join()
    

if __name__ == '__main__':
  from sys import argv
  main(argv)
