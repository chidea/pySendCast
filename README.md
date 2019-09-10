# pySendCast
A pure Python cross-platform program to send and receive data over local area network(LAN) with on-the-fly gzip streaming and broadcasting

### How to install
```
pip install pySendCast
```

### How to use
```
sendcast send [file or messages...]
  sends without PIN.
sendcast send <-p|--pin> [file or messages...]
  sends with newly generated PIN
sendcast send <-up|--userpin> <user PIN> [file or messages...]
  sends with user specified PIN
```
file or message can be any of
- nothing : check up each other's ip address
- file path : send and receive files with glob searching (ex. `*.py`)
- url : receiver opens default web browser with it
- message : simple text messages

```
sendcast recv
  receives without PIN
sendcast recv <user PIN>
  receives with user specified PIN
sendcast recv <n|new|g|gen>
  receives with newly generated PIN
```

### How to use with usecases
1. checkup IP
- Sender : 192.168.0.10
```shell
$ sendcast send
192.168.0.11
```
- Receiver : 192.168.0.11
```shell
$ sendcast recv
192.168.0.10
```

2. Send message
- Sender
```shell
$ sendcast send hello
192.168.0.11
```
- Receiver
```shell
$ sendcast recv
192.168.0.10
hello
```

3. General usecase : send two files without PIN. The First non-PIN receiver on network takes the file
- Sender
```shell
$ sendcast send a.txt b.txt
192.168.0.11
sending a.txt
sending b.txt
```
- Receiver
```shell
$ sendcast recv
192.168.0.10
extracting a.txt (23 bytes)
extracting a.txt done (23 bytes, 0.0000413 seconds, 0.557163 MB/s)
extracting b.txt (27 bytes)
extracting b.txt done (27 bytes, 0.0000405 seconds, 0.666000 MB/s)
```

4. generated PIN usecase : send with newly generated PIN. receiver must know PIN to receive the file (be aware that its stream itself is **not securely encrypted**.)
- Sender
```shell
$ sendcast send -p a.txt b.txt
generated PIN : 3061
192.168.0.11
sending a.txt
sending b.txt
```
- Receiver
```shell
$ sendcast recv 3061
192.168.0.10
extracting a.txt (23 bytes)
extracting a.txt done (23 bytes, 0.0000413 seconds, 0.557163 MB/s)
extracting b.txt (27 bytes)
extracting b.txt done (27 bytes, 0.0000405 seconds, 0.666000 MB/s)
```

5. user PIN usecase : send with user PIN. receiver must know PIN to receive the file (be aware that its stream itself is **not securely encrypted**.)
- Sender
```shell
$ sendcast send -up 9999 a.txt b.txt
user PIN : 9999
192.168.0.11
sending a.txt
sending b.txt
```
- Receiver
```shell
$ sendcast recv 9999
192.168.0.10
extracting a.txt (23 bytes)
extracting a.txt done (23 bytes, 0.0000413 seconds, 0.557163 MB/s)
extracting b.txt (27 bytes)
extracting b.txt done (27 bytes, 0.0000405 seconds, 0.666000 MB/s)
```

6. receiver generated PIN usecase : send with receiver created user PIN. sender must know PIN to send the file (be aware that its stream itself is **not securely encrypted**.)
- Receiver
```shell
$ sendcast recv n
generated PIN : 2342
192.168.0.10
extracting a.txt (23 bytes)
extracting a.txt done (23 bytes, 0.0000413 seconds, 0.557163 MB/s)
extracting b.txt (27 bytes)
extracting b.txt done (27 bytes, 0.0000405 seconds, 0.666000 MB/s)
```
- Sender
```shell
$ sendcast send -up 2342 a.txt b.txt
user PIN : 2342
192.168.0.11
sending a.txt
sending b.txt
```

### special usecase
- send/recv from Android
  - using [Termux](https://play.google.com/store/apps/details?id=com.termux&hl=en)

### Security note
The receiver takes any gzip tar stream from port number 18902.
Becuase this stream is not encrypted, it can be captured with network tools or can be easily targeted for hacking.
**Any responses from security issues are not taken by developer.**
