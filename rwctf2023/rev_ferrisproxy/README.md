## [RWCTF 2023] Ferris' proxy

Writeup by [@nneonneo](https://github.com/nneonneo).

Ferris' proxy was a reversing challenge in Real World CTF 2023, with a score of 188 and a total of 22 solves.

We are provided with a pair of large (40+ MB) binaries, `client` and `server`, along with a packet capture.

Opening both binaries in IDA, we can see that they are clearly Rust binaries with debug symbols - that's why they're so big. Both binaries are using the tokio framework to perform asynchronous I/O, which also makes the program flow a lot harder to follow.

I focused primarily on reversing the server. In the server, we can immediately see some interesting code in the `lib::protocol` namespace and the `server` namespace; these are likely the parts that are challenge-specific. `server` contains the functions `server::main` and `server::process_connection`, while `lib::protocol` consist of the following crates:

- `lib::protocol::crypto`
- `lib::protocol::mux`
- `lib::protocol::rc4`
- `lib::protocol::socket`
- `lib::protocol::socks5`

By running both binaries under `strace`, we can determine that the server opens TCP port 8888, the client connects to that port, and then the client opens TCP port 12345. Based on the `socks5` reference in the binary, we can guess that the client exports a SOCKS5 proxy, and then encrypts the traffic going to the server. We can confirm this by running `http_proxy=socks5://localhost:12345 curl http://google.com -vvvv` and seeing a bunch of traffic between client and server.

 `server::main`, and the corresponding async implementation `server::main::_{{closure}}`, calls the following functions in order, many of which are async:

- `serde_yaml::de::from_str`
- `TcpListener::bind` with 8888
- `TcpListener::accept`
- `lib::protocol::rc4::Rc4<T,V>::new`, then `lib::protocol::rc4::Rc4<T,V>::process_transfer`
- `lib::protocol::mux::MuxCore<T>::listen`
- `lib::protocol::mux::MuxCore<T>::process_transfer`
- `lib::protocol::mux::MuxListener::accept`
- `server::process_connection` (which ends up calling the async implementation `server::process_connection::_{{closure}}`), which calls:
    - `lib::protocol::mux::MuxChannel<T>::set_from`
    - `lib::protocol::mux::MuxChannel<T>::process_transfer`
    - `lib::protocol::crypto::Crypto<T,V>::new`
    - `lib::protocol::crypto::Crypto<T,V>::key_exchange`
    - `lib::protocol::crypto::Crypto<T,V>::process_transfer`
    - `lib::protocol::socks5::Socks5Server<T,V>::new`
    - `lib::protocol::socks5::Socks5Server<T,V>::process_connection`
    - `lib::protocol::socket::TcpClient<T>::connect`
    - `lib::protocol::socks5::Socks5Server<T,V>::process_response`
    - and so on.

This tells us a lot! We already know it's a SOCKS5 implementation, so we can immediately infer that it is likely using RC4 to secure the connection with the client, then multiplexing (muxing) multiple SOCKS5 connections over a single socket connection. We can also see that each SOCKS5 connection (a channel) is secured with a second cryptographic protocol which involves a key exchange.

We can also see that it loads some YAML data. By stripping the binaries (to remove distracting debug strings) and running `strings`, we can find the following YAML blobs:

server:

```
pubkey: |
    -----BEGIN RSA PUBLIC KEY-----
    MIIBCgKCAQEAvdxgyDTzOh19vjTd2ws58q4tqwxw1XGpswP6zw14vTG9obtWKanp
    OJJv5H+DCg7KzlP90+ZnHceZAPNLO5gVpRmiLYP7MunbIdlzqClRB3GWMq20gG5G
    K0/QqCyzPyZYqW7GpSnp5FvSZRwdIfr8L/6wMFyfSDEnOEUJL45/0CrgT4XF3632
    gCCjTtC/oqlC92rBTNghfA12V8vKSwMTMtjwyS7W9CP61w1kSJlpQXCFga4YO5Qw
    NFMVlww9YuTJjJb8ZsoaNRfAa4e4nrSt11uy1rIQ9gESA4D6E2e5WZuz/SWykjfl
    JO32sui3ZCV2LM30/PTsJou7Zn1EONX3AQIDAQAB
    -----END RSA PUBLIC KEY-----
mkey: explorer 
privkey: |
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDbfWw2tfpbGVCl
    +zLy7pVH2vDgfiVj3d+ykCZd5+MOFCFgI8z5LKkG8iBv/D1/wAaQTBSUNDF9kIKX
    PvYYC5L2OuWyqD0ulIxn48kA7QENaKywkIm3LIQ1b/1VU+kksDRJJ5i5NgnzhYMB
    yOxvRP75X3tNeVKKr2y9e3XosPEJAmNFe/07VRMGQOkYZmadHjEuJBP4/Hoo6oCy
    slwAXQQlqOLloF8dVB2tdDCCarw8Sx+e+naJAItnaIM8uUZtFqF0V6KBddPgvpS+
    OlsWv/0g28Nvb69CRGXvOUdW1QAxHhfmyZbacccfljJOLVw68wWw36g8bGAEalKp
    gLGY/Ag3AgMBAAECggEADbfJC6JUA12RrM4GYSiIK/WDGITJ0XQMhxx7SWM0zax0
    aY3TQb+I0OZRIK6jKVjXEC2xG5InhbGCd/F3cAlJJhqIQKJDMKYYIGYcKfKmHjBs
    mpxt/wTJPo3BR5P2/lQE8I2I/gpilNXDWlk0bb/iL7PIAQ+UGRbdtPoCZIiqh+WA
    qElaJ4LHXgKBXUpozfEtUa383IcwsQdB1BSwMOnJ5YFrplhx6fTgJ6noFB4eLp7h
    SCSR2018r11UAANqWbc7a40TtLpWUmh3AExCeQACI1RloTSCRWYsXrxFMH6ZGDvE
    K+Q9LS+jtkPCtOrbr+j8FU0Dgxh/5P0I2xR4hcgAAQKBgQDkcnwcaWRZv0uFxAtj
    q3pVelWuu3uapwroO9asmeWsmL3LQeW22X5CNy1gYOlhyG6FqfMLOmzhCicFYX45
    6EiDJpyX/LVcSDmzmTDwI25uEunhyhVATJWqwaITdLrJf8KDqqO8bvUHc/wB//2T
    OTWpUB542DZJ2A8aServjR6ErwKBgQD19l+5xCHLOldtV56hbAQnhhl8lUAL/mBq
    wXNrDNeqmDYFJ3kkHWk5raXUQR41qAubhKnLUJ4qj6FIBcRmsrTMITMWZ9/GzJhK
    mNU+nync2IlSS7g3Vyee3wz1Fd2dRA3NwZ9JVK+xTSKgw1a/VXKcfC+iYnXmVIxa
    3cCIZ9Um+QKBgQDE34Dj/1OzIG+WbPgfwiTgS1hSCFKiWfjFYORFxS8wykUuSLEO
    Hmt35xNc7sfSNChDWs4QzB4O5m/wbC+a+fqbxAfJ18f4KmpHw+pv2SkPBY+3vS8J
    Rbbp/IuP1tYuVsMsMz9+YeUasjLpClLesLv1GQ3ZuQM4KlIBptgn7+bwEwKBgQC1
    ZDk8etShWClZziCC03JM46ywIDHXpoXctUY1UIdMnGxaaL4CUF5l1xZQ7qUk1QWa
    b7/43T+IC9zZjMdHJcwILwPKJlj197TobsX1JNRutpKvSoBU78WceMrJhJKnhKTZ
    dU3PetEHZOeAwA6dlJqtpThL/WkNsJTB/oAbGNgtoQKBgG4ytUXXwp61VHm/3Pon
    9d6z5o02AQVCppJRcJwehbAm14813G/jPfjwM+KZ2ikhs+eW1peWhBrCo+M5/u5T
    bxeDm9cbLMewkYNIdvUxtaBb+fJtIBAngAL2HEhqBdUFoQI+lr+F802UO2aM8Sg+
    n82S/+EJZomQ7hhO7qnLtxkI
    -----END PRIVATE KEY-----
```

client:

```
pubkey: |
    -----BEGIN RSA PUBLIC KEY-----
    MIIBCgKCAQEA231sNrX6WxlQpfsy8u6VR9rw4H4lY93fspAmXefjDhQhYCPM+Syp
    BvIgb/w9f8AGkEwUlDQxfZCClz72GAuS9jrlsqg9LpSMZ+PJAO0BDWissJCJtyyE
    NW/9VVPpJLA0SSeYuTYJ84WDAcjsb0T++V97TXlSiq9svXt16LDxCQJjRXv9O1UT
    BkDpGGZmnR4xLiQT+Px6KOqAsrJcAF0EJaji5aBfHVQdrXQwgmq8PEsfnvp2iQCL
    Z2iDPLlGbRahdFeigXXT4L6UvjpbFr/9INvDb2+vQkRl7zlHVtUAMR4X5smW2nHH
    H5YyTi1cOvMFsN+oPGxgBGpSqYCxmPwINwIDAQAB
    -----END RSA PUBLIC KEY-----
mkey: explorer
privkey: |
    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC93GDINPM6HX2+
    NN3bCznyri2rDHDVcamzA/rPDXi9Mb2hu1Ypqek4km/kf4MKDsrOU/3T5mcdx5kA
    80s7mBWlGaItg/sy6dsh2XOoKVEHcZYyrbSAbkYrT9CoLLM/JlipbsalKenkW9Jl
    HB0h+vwv/rAwXJ9IMSc4RQkvjn/QKuBPhcXfrfaAIKNO0L+iqUL3asFM2CF8DXZX
    y8pLAxMy2PDJLtb0I/rXDWRImWlBcIWBrhg7lDA0UxWXDD1i5MmMlvxmyho1F8Br
    h7ietK3XW7LWshD2ARIDgPoTZ7lZm7P9JbKSN+Uk7fay6LdkJXYszfT89Owmi7tm
    fUQ41fcBAgMBAAECggEAWyGJru+Dg/Sd44t6peY4lVy3fO/GxRz+qHeTjojX2HAk
    ppnGHM96q3XWkWYHHu/Ets6n+msQOcIRldwx01QHp6yrJI/CJkkLrq6yjhfu1dTW
    lFK+XhsQQT/ZVq/GBdzBF+qdHLAGnV7ZmUCqVyIipGLqbPw4VC2Ltr2kUBhlDySA
    A+gCnUrPyVi6O9OFcyDepKMy481gZLLijakINejYrsbdCInz2omHq12w/50tuFt1
    s4XMWJN+AW0g1Hx+tTk2jDX1Wqg/htmJhjGqTj02GLJ/CJQjRodEdA7mx3HGwhis
    igeZgHTdPgP1B5Z9NXwUg9Qxln72D4mGhLCGYcw8VQKBgQD6+oltv1i44BO/ROUJ
    kZPTLWeoBrxP2OOli4aOSilLifeGrUQOSUtvcFHOxzy5RrhvX89f3GnklXcGyHXD
    03wg0/hqL0HM1EzNLmWkJW0Ng5WRFFgfcQIKbWBK9SHhAmKzkHtZPq6NwN8MbZUF
    vndxDtcSOdH0/TbMtCMYYs0MswKBgQDBqM7QxWT6qebCU4YOV+5uwnP+hAunsWkv
    VW7pHgiPnZ8ARRZ9iFIqqiVRvKeeyZBEK22eOJNguz6Cqfz2451D/AHA7sXht+1D
    9GCE/ebvUw+lPNQIRKkAgwQ8Dx+R6ikaUGzUKYhmWYJ5xgS9ZALZ+k4+rSjFg9jV
    jFjT7xQvewKBgHo9bJI3kE77VKLkO2ndrdI9Wy9LmIyLZtVKj87d8B8Ko7TEz1Dm
    AgfU/QNppvnWqB4W3DokcK8U3VRAbptidiLHG0ccnT/WZ1HIN1kroWHjpQV0kzc9
    I3FQtIXNvyKItuoehPWCwiHovrqe5OZXTnWSdM47uzdH3Vj2o+FMvfJhAoGAQvus
    bTGZd8oEcvqIx7VKVy0TCdmKXnpSs3iNYDxvIZ2XPXSoDst0ACXRuq/SGm4FZE7R
    H4TaFP8u4+sAADVCVB16Tc1IzIXdnz+LkvRvSCAmrTSY8jMtcWvfrxZcCRBBH0Tq
    H4guEZisNIp1YTySb+rP3YXvMEImYdalcsii5rkCgYEAimnWJ5aFN3TDt3h76CL3
    nRQegnzekJBjXZfcrHdExkgNChWjiz+WU/FW/Z87xMxtfIEwwzzIQHxbKZhgzO/U
    p2eXdqH59DvauggbiS3h4p9k2kxWTocztarvdftMW0ncmA4yCKiUQEmWD784JCyx
    OupNNfr2rgViWggVBEtJUIg=
    -----END PRIVATE KEY-----
```

### Breaking the Mux encryption

The outer layer of encryption appears to be Rc4. Per the YAML files, the key might be `explorer` (the `mkey`). We can confirm this by decompiling `lib::protocol::rc4::Rc4<T,V>::new`, which calls `openssl::symm::Crypter::new`. By setting a breakpoint on this function in GDB, we can dump out the `key` argument. With DWARF debug data, GDB does an excellent job of locating and presenting the Rust function arguments:

```
gef➤  break openssl::symm::Crypter::new 
Breakpoint 1 at 0x1e1b71: file src/symm.rs, line 498.
gef➤  run
[...]
[start ./client]
Thread 1 "server" hit Breakpoint 1, openssl::symm::Crypter::new (t=..., mode=openssl::symm::Mode::Encrypt, key=..., iv=...) at src/symm.rs:498
[#0] 0x555555735b71 → openssl::symm::Crypter::new(t=openssl::symm::Cipher (
  0x7ffff7f044e0
), mode=openssl::symm::Mode::Encrypt, key=&[u8] {
  data_ptr: 0x555555b680a0,
  length: 0x8
}, iv=core::option::Option<&[u8]>::None)
[#1] 0x5555556029fe → lib::protocol::rc4::Rc4<tokio::net::tcp::stream::TcpStream, tokio::io::util::mem::DuplexStream>::new<tokio::net::tcp::stream::TcpStream, tokio::io::util::mem::DuplexStream>(from=tokio::net::tcp::stream::TcpStream {
  io: tokio::io::poll_evented::PollEvented<mio::net::tcp::stream::TcpStream> {
    io: core::option::Option<mio::net::tcp::stream::TcpStream>::Some(mio::net::tcp::stream::TcpStream {
        inner: mio::io_source::IoSource<std::net::tcp::TcpStream> {
          state: mio::sys::unix::IoSourceState,
          inner: std::net::tcp::TcpStream (
            std::sys_common::net::TcpStream {
              inner: std::sys::unix::net::Socket (
                std::sys::unix::fd::FileDesc (
                  std::os::fd::owned::OwnedFd {
                    fd: 0xa
                  }
                )
              )
            }
          ),
          selector_id: mio::io_source::SelectorId {
            id: core::sync::atomic::AtomicUsize {
              v: core::cell::UnsafeCell<usize> {
                value: 0x1
              }
            }
          }
        }
      }),
    registration: tokio::runtime::io::registration::Registration {
      handle: tokio::runtime::io::Handle {
        inner: alloc::sync::Arc<tokio::runtime::io::Inner> {
          ptr: core::ptr::non_null::NonNull<alloc::sync::ArcInner<tokio::runtime::io::Inner>> {
            pointer: 0x555555b49370
          },
          phantom: core::marker::PhantomData<alloc::sync::ArcInner<tokio::runtime::io::Inner>>
        }
      },
      shared: tokio::util::slab::Ref<tokio::runtime::io::scheduled_io::ScheduledIo> {
        value: 0x555555b4ea90
      }
    }
  }
}, to=tokio::io::util::mem::DuplexStream {
  read: alloc::sync::Arc<tokio::loom::std::parking_lot::Mutex<tokio::io::util::mem::Pipe>> {
    ptr: core::ptr::non_null::NonNull<alloc::sync::ArcInner<tokio::loom::std::parking_lot::Mutex<tokio::io::util::mem::Pipe>>> {
      pointer: 0x555555b68d10
    },
    phantom: core::marker::PhantomData<alloc::sync::ArcInner<tokio::loom::std::parking_lot::Mutex<tokio::io::util::mem::Pipe>>>
  },
  write: alloc::sync::Arc<tokio::loom::std::parking_lot::Mutex<tokio::io::util::mem::Pipe>> {
    ptr: core::ptr::non_null::NonNull<alloc::sync::ArcInner<tokio::loom::std::parking_lot::Mutex<tokio::io::util::mem::Pipe>>> {
      pointer: 0x555555b68d80
    },
    phantom: core::marker::PhantomData<alloc::sync::ArcInner<tokio::loom::std::parking_lot::Mutex<tokio::io::util::mem::Pipe>>>
  }
}, key=&[u8] {
  data_ptr: 0x555555b680a0,
  length: 0x8
})
gef➤  x/s 0x555555b680a0
0x555555b680a0:	"explorer"
```

This function gets hit twice, once for each direction of the connection.

To decrypt the pcap, we first dump the contents in a more manageable format (to [`dump1.txt`](dump1.txt)):

`tshark -d 'tcp.port==8888,data' -Tfields -Y 'tcp.len > 0' -e 'tcp.stream' -e 'tcp.dstport' -e 'data.data' -r 'flag2_a027c9cbb41e22180def5f6532089927.pcapng' > dump1.txt`

Then, we can use a simple Python script to decrypt each packet with RC4:

```
from Crypto.Cipher import ARC4
from collections import defaultdict
import struct

ciphers = defaultdict(lambda: ARC4.new(b"explorer"))
streams = defaultdict(lambda: bytearray())

for row in open("dump1.txt"):
    stream, dstport, data = row.split()
    print(stream, dstport, ciphers[stream, dstport].decrypt(bytes.fromhex(data)).hex(), sep="\t")
```

The data thus dumped looks like this:

```
0	8888	000000080000000000000000
0	8888	000000080000000000000001
0	50671	000000080000000000000000000000080000000000000001
0	50671	0000004800000001000000010100bb6c4b7677bee4b0a9310696a0629d00370d0cf4d48702b3d8d4e49bc89b0ed450dba1349f21c32a98000f753e39af2299e82404fddd482290c3d8f74c7c000000480000000100000001a1cd7638ba839cccc0e605fe3f8f1be666e84fabe507d451097ef3d19399de8f0d5b60709c20806b4e0fb8f0c41ba021a086d81e1666aad411bb6858f0cfb22800000048000000010000000108e85dae9cdf93706acc01296eb505cd372f8b7bc7f98619f70a1cbcb129aa3ecc3f1f3716070aa0e364fff54bf842a2d61c48188c623177fc037d343bf25b040000004800000001000000019c7e26c52ea5f69638a19a7455a7639583ad2ed2c93883123bcc442e4a0caa6126c67ad9b8a9c43515cc226741517fc12b55a9a7995ec16c210fe8cdc8b9df6c0000000a0000000100000001430e
0	50671	0000004800000001000000000100b23257fec2b63f599eb532763ac87781fddc3cc3b20da741cae5f1da705e9074a9ffb0e39198cf12271b354332a21ec5ed895abd26727b5e0cadd5b6141e0000004800000001000000000b778bb9bee681073afe9feac5f83b41879f3f34d3c718887a868d23299ce4aac7757ca7176cf414eb62240a8f5822e60349dc944e178b83a7b662ef9348e2040000004800000001000000005e46fcd4eca90600e4860f0504f633c92af969e6dd8b58c489a9a6068c8c6379c940b23ff19f55deec69c887e9e1c06bc8b09f39fa9708d8d1554597373af8ad0000004800000001000000004db4b9036aa89989a658142ca779d8dae49ee3eac14e71899268c970b4a331006cdfb31167568d11b3c595a0649cb4f8782a9b8b395eaa8c66287fe94b5d22f20000000a0000000100000000aca5
0	8888	00000048000000010000000001001db2ee547837c2b0394f9316a3c672109c854769d9627ce715aa82ae76af4fc7d468903ffa4f7c9d4afcf139528ceb24cb5f64a192287282ee7fd076992f000000480000000100000000e73f0a730b98e032e90afaf73b8ddab1e821432c3e1c2c51396914f53fb304f26cbc8f85ec68462ff85dfb0979648d43003291ccb9418e7b4016f5d3325d4083000000480000000100000000d44c5aff410f28c841fb51c2e982244d7f7370fb6b73d6e5caba56c1b4b8f96bea190aa8d66e7e37d76fe2e5fef7f78b0de90e12eefda3a36177583412ca074e00000048000000010000000096a1796af867e440a72ee81e36e05f3b73c3341f6166b804bf83c3d0b47df74cc77405595ce44d3ccfb739496b8acb78fdb02bcd510851b3e3de015fc06eadb40000000a00000001000000000f8e
0	8888	0000004800000001000000010100320b119809b793abf357a7f78b0742ee93a957e563a5a94fdb09804e89596f2597a2cb9ae9f5161d5fda88ff050e47b1d28bebc6563465d2e7959e8a624a000000480000000100000001cd39b2053c17021f93030e3b9bc7149ff5423faf64693932f76a8dbffa526fff7c076845b1d31967efca0b56b066e8bacedc1927e629c6d0e87f61bf14ee3039000000480000000100000001053d668ef1855426257ce68cdbc2f66919a2f9efbcb632daa6170cb8246ab7a2348032f48cefdbc3aadcee6b9ab867371346bbe90fd69d213705ed1de38922b300000048000000010000000145bbbf8e0b10c5436e5974f46426d3efdbeaba819ea5d049bb420219a426336e14bc36e5753cb71fb21a2b78f699918a0045a8badddd69646ed65a59e17feec80000000a0000000100000001b30c
0	50671	0000002800000001000000002accc966ccaf48a147471171fb9589c95c561100d6548ad979f328e43bcfe075
0	8888	000000280000000100000001503fdd267309866142ae96b3197515b72ccd766dedbc09d61c25f0c3fa79ebd4
0	8888	0000002800000001000000002accc966ccaf48a147471171fb9589c95c561100d6548ad979f328e43bcfe075
```

This looks like a very simple binary protocol. Each packet appears to start with a 4-byte big-endian length, a 4-byte command code (0, 1 or 2), and a 4-byte integer that starts from zero and increments occasionally (likely a channel identifier - to identify the individual multiplexed channels), and finally a variable-length payload. Command 0 seems to open a new channel by ID, command 1 provides data that flows to that channel, and command 2 seems to close a channel.

Armed with this information, we can expand our decoder to demux the channel contents ([`dump2.py`](dump2.py)):

```
from Crypto.Cipher import ARC4
from collections import defaultdict
import struct

ciphers = defaultdict(lambda: ARC4.new(b"explorer"))
streams = defaultdict(lambda: bytearray())

for row in open("dump1.txt"):
    stream, dstport, data = row.split()
    streams[stream, dstport] += ciphers[stream, dstport].decrypt(bytes.fromhex(data))
    while len(streams[stream, dstport]) >= 4:
        plen, = struct.unpack(">I", streams[stream, dstport][:4])
        if len(streams[stream, dstport]) < 4 + plen:
            break
        pkt = streams[stream, dstport][4:4+plen]
        streams[stream, dstport] = streams[stream, dstport][4+plen:]
        assert len(pkt) >= 8
        cmd, mid = struct.unpack(">II", pkt[:8])
        print(stream, dstport, cmd, mid, pkt[8:].hex(), sep="\t")
```

This produces output like this ([`dump2.txt`](dump2.txt)):

```
0	8888	0	0	
0	8888	0	1	
0	50671	0	0	
0	50671	0	1	
0	50671	1	1	0100bb6c4b7677bee4b0a9310696a0629d00370d0cf4d48702b3d8d4e49bc89b0ed450dba1349f21c32a98000f753e39af2299e82404fddd482290c3d8f74c7c
0	50671	1	1	a1cd7638ba839cccc0e605fe3f8f1be666e84fabe507d451097ef3d19399de8f0d5b60709c20806b4e0fb8f0c41ba021a086d81e1666aad411bb6858f0cfb228
0	50671	1	1	08e85dae9cdf93706acc01296eb505cd372f8b7bc7f98619f70a1cbcb129aa3ecc3f1f3716070aa0e364fff54bf842a2d61c48188c623177fc037d343bf25b04
0	50671	1	1	9c7e26c52ea5f69638a19a7455a7639583ad2ed2c93883123bcc442e4a0caa6126c67ad9b8a9c43515cc226741517fc12b55a9a7995ec16c210fe8cdc8b9df6c
0	50671	1	1	430e
0	50671	1	0	0100b23257fec2b63f599eb532763ac87781fddc3cc3b20da741cae5f1da705e9074a9ffb0e39198cf12271b354332a21ec5ed895abd26727b5e0cadd5b6141e
0	50671	1	0	0b778bb9bee681073afe9feac5f83b41879f3f34d3c718887a868d23299ce4aac7757ca7176cf414eb62240a8f5822e60349dc944e178b83a7b662ef9348e204
0	50671	1	0	5e46fcd4eca90600e4860f0504f633c92af969e6dd8b58c489a9a6068c8c6379c940b23ff19f55deec69c887e9e1c06bc8b09f39fa9708d8d1554597373af8ad
0	50671	1	0	4db4b9036aa89989a658142ca779d8dae49ee3eac14e71899268c970b4a331006cdfb31167568d11b3c595a0649cb4f8782a9b8b395eaa8c66287fe94b5d22f2
0	50671	1	0	aca5
0	8888	1	0	01001db2ee547837c2b0394f9316a3c672109c854769d9627ce715aa82ae76af4fc7d468903ffa4f7c9d4afcf139528ceb24cb5f64a192287282ee7fd076992f
0	8888	1	0	e73f0a730b98e032e90afaf73b8ddab1e821432c3e1c2c51396914f53fb304f26cbc8f85ec68462ff85dfb0979648d43003291ccb9418e7b4016f5d3325d4083
0	8888	1	0	d44c5aff410f28c841fb51c2e982244d7f7370fb6b73d6e5caba56c1b4b8f96bea190aa8d66e7e37d76fe2e5fef7f78b0de90e12eefda3a36177583412ca074e
0	8888	1	0	96a1796af867e440a72ee81e36e05f3b73c3341f6166b804bf83c3d0b47df74cc77405595ce44d3ccfb739496b8acb78fdb02bcd510851b3e3de015fc06eadb4
0	8888	1	0	0f8e
0	8888	1	1	0100320b119809b793abf357a7f78b0742ee93a957e563a5a94fdb09804e89596f2597a2cb9ae9f5161d5fda88ff050e47b1d28bebc6563465d2e7959e8a624a
0	8888	1	1	cd39b2053c17021f93030e3b9bc7149ff5423faf64693932f76a8dbffa526fff7c076845b1d31967efca0b56b066e8bacedc1927e629c6d0e87f61bf14ee3039
0	8888	1	1	053d668ef1855426257ce68cdbc2f66919a2f9efbcb632daa6170cb8246ab7a2348032f48cefdbc3aadcee6b9ab867371346bbe90fd69d213705ed1de38922b3
0	8888	1	1	45bbbf8e0b10c5436e5974f46426d3efdbeaba819ea5d049bb420219a426336e14bc36e5753cb71fb21a2b78f699918a0045a8badddd69646ed65a59e17feec8
0	8888	1	1	b30c
0	50671	1	0	2accc966ccaf48a147471171fb9589c95c561100d6548ad979f328e43bcfe075
0	8888	1	1	503fdd267309866142ae96b3197515b72ccd766dedbc09d61c25f0c3fa79ebd4
0	8888	1	0	2accc966ccaf48a147471171fb9589c95c561100d6548ad979f328e43bcfe075
0	8888	1	0	0000001023a5457e1fa2e2f4a23242b1e61a597d1458bee4871e6f44e929682001472830
0	50671	1	1	503fdd267309866142ae96b3197515b72ccd766dedbc09d61c25f0c3fa79ebd4
```

### Breaking the channel encryption

We know that the individual channels start with some kind of cryptographic key exchange. Decompiling `lib::protocol::crypto::Crypto<T,V>::key_exchange::_{{closure}}`, we see calls to:

- `rsa::padding::PaddingScheme::new_pkcs1v15_encrypt`
- `<rsa::key::RsaPublicKey as rsa::key::PublicKey>::encrypt`
- `rsa::padding::PaddingScheme::new_pkcs1v15_encrypt`
- `rsa::key::RsaPrivateKey::decrypt`
- `core::iter::adapters::zip::zip`, `core::iter::traits::iterator::Iterator::map`, `core::iter::traits::iterator::Iterator::collect`
- `openssl::sha::sha256`
- `tokio::io::util::async_write_ext::AsyncWriteExt::write_all`

We also have a closure function `lib::protocol::crypto::Crypto<T,V>::key_exchange::_{{closure}}::_{{closure}}` which simply XORs two bytes. From this, we can infer that the key exchange protocol probably consists of exchanging random bytes encrypted with the counterparty's RSA key, then XORing those bytes together to get a shared key, and finally exchanging the SHA-256 of those keys for verification. Indeed, if we look at the initial messages of a channel:

```
0	50671	1	0	0100b23257fec2b63f599eb532763ac87781fddc3cc3b20da741cae5f1da705e9074a9ffb0e39198cf12271b354332a21ec5ed895abd26727b5e0cadd5b6141e
0	50671	1	0	0b778bb9bee681073afe9feac5f83b41879f3f34d3c718887a868d23299ce4aac7757ca7176cf414eb62240a8f5822e60349dc944e178b83a7b662ef9348e204
0	50671	1	0	5e46fcd4eca90600e4860f0504f633c92af969e6dd8b58c489a9a6068c8c6379c940b23ff19f55deec69c887e9e1c06bc8b09f39fa9708d8d1554597373af8ad
0	50671	1	0	4db4b9036aa89989a658142ca779d8dae49ee3eac14e71899268c970b4a331006cdfb31167568d11b3c595a0649cb4f8782a9b8b395eaa8c66287fe94b5d22f2
0	50671	1	0	aca5
0	8888	1	0	01001db2ee547837c2b0394f9316a3c672109c854769d9627ce715aa82ae76af4fc7d468903ffa4f7c9d4afcf139528ceb24cb5f64a192287282ee7fd076992f
0	8888	1	0	e73f0a730b98e032e90afaf73b8ddab1e821432c3e1c2c51396914f53fb304f26cbc8f85ec68462ff85dfb0979648d43003291ccb9418e7b4016f5d3325d4083
0	8888	1	0	d44c5aff410f28c841fb51c2e982244d7f7370fb6b73d6e5caba56c1b4b8f96bea190aa8d66e7e37d76fe2e5fef7f78b0de90e12eefda3a36177583412ca074e
0	8888	1	0	96a1796af867e440a72ee81e36e05f3b73c3341f6166b804bf83c3d0b47df74cc77405595ce44d3ccfb739496b8acb78fdb02bcd510851b3e3de015fc06eadb4
0	8888	1	0	0f8e
0	50671	1	0	2accc966ccaf48a147471171fb9589c95c561100d6548ad979f328e43bcfe075
0	8888	1	0	2accc966ccaf48a147471171fb9589c95c561100d6548ad979f328e43bcfe075
0	8888	1	0	0000001023a5457e1fa2e2f4a23242b1e61a597d1458bee4871e6f44e929682001472830
0	50671	1	0	00000010ca9a58d5c953664da8d49e38818bb2e124958322ed732307bb0f1f2d47eb0574
```

we can see clearly two 256-byte blobs followed by two identical hash-sized values.

With Python, we can decrypt these blobs using the private keys from the YAML configurations we found, and verify that they indeed both decrypt to 16-byte blobs after removing PKCS v1.5 padding. We can also verify that the SHA256 of the XOR of these blobs is exactly the value that is exchanged at the end.

The subsequent packets have a 4-byte length field, followed by 16+length bytes of data.

In `lib::protocol::crypto::Crypto<T,V>::process_data_dec_in::_{{closure}}` we see a call to `openssl::symm::Cipher::aes_128_cbc`, which tells us that the rest of the data is probably encrypted with AES-128 in CBC mode.  By setting a breakpoint on `openssl::symm::Crypter::new` while capturing packets on our local setup, we can confirm that the IV for the cipher is just the first 16 bytes of each packet.

All that's left to do is extract out the keys and decrypt the individual channels, which we can do with [this Python script](dump3.py):

```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util.Padding import unpad
import os
import hashlib
from collections import defaultdict
from io import BytesIO
import struct

sentinel = os.urandom(256)

rsa0 = RSA.importKey("""-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC93GDINPM6HX2+
NN3bCznyri2rDHDVcamzA/rPDXi9Mb2hu1Ypqek4km/kf4MKDsrOU/3T5mcdx5kA
80s7mBWlGaItg/sy6dsh2XOoKVEHcZYyrbSAbkYrT9CoLLM/JlipbsalKenkW9Jl
HB0h+vwv/rAwXJ9IMSc4RQkvjn/QKuBPhcXfrfaAIKNO0L+iqUL3asFM2CF8DXZX
y8pLAxMy2PDJLtb0I/rXDWRImWlBcIWBrhg7lDA0UxWXDD1i5MmMlvxmyho1F8Br
h7ietK3XW7LWshD2ARIDgPoTZ7lZm7P9JbKSN+Uk7fay6LdkJXYszfT89Owmi7tm
fUQ41fcBAgMBAAECggEAWyGJru+Dg/Sd44t6peY4lVy3fO/GxRz+qHeTjojX2HAk
ppnGHM96q3XWkWYHHu/Ets6n+msQOcIRldwx01QHp6yrJI/CJkkLrq6yjhfu1dTW
lFK+XhsQQT/ZVq/GBdzBF+qdHLAGnV7ZmUCqVyIipGLqbPw4VC2Ltr2kUBhlDySA
A+gCnUrPyVi6O9OFcyDepKMy481gZLLijakINejYrsbdCInz2omHq12w/50tuFt1
s4XMWJN+AW0g1Hx+tTk2jDX1Wqg/htmJhjGqTj02GLJ/CJQjRodEdA7mx3HGwhis
igeZgHTdPgP1B5Z9NXwUg9Qxln72D4mGhLCGYcw8VQKBgQD6+oltv1i44BO/ROUJ
kZPTLWeoBrxP2OOli4aOSilLifeGrUQOSUtvcFHOxzy5RrhvX89f3GnklXcGyHXD
03wg0/hqL0HM1EzNLmWkJW0Ng5WRFFgfcQIKbWBK9SHhAmKzkHtZPq6NwN8MbZUF
vndxDtcSOdH0/TbMtCMYYs0MswKBgQDBqM7QxWT6qebCU4YOV+5uwnP+hAunsWkv
VW7pHgiPnZ8ARRZ9iFIqqiVRvKeeyZBEK22eOJNguz6Cqfz2451D/AHA7sXht+1D
9GCE/ebvUw+lPNQIRKkAgwQ8Dx+R6ikaUGzUKYhmWYJ5xgS9ZALZ+k4+rSjFg9jV
jFjT7xQvewKBgHo9bJI3kE77VKLkO2ndrdI9Wy9LmIyLZtVKj87d8B8Ko7TEz1Dm
AgfU/QNppvnWqB4W3DokcK8U3VRAbptidiLHG0ccnT/WZ1HIN1kroWHjpQV0kzc9
I3FQtIXNvyKItuoehPWCwiHovrqe5OZXTnWSdM47uzdH3Vj2o+FMvfJhAoGAQvus
bTGZd8oEcvqIx7VKVy0TCdmKXnpSs3iNYDxvIZ2XPXSoDst0ACXRuq/SGm4FZE7R
H4TaFP8u4+sAADVCVB16Tc1IzIXdnz+LkvRvSCAmrTSY8jMtcWvfrxZcCRBBH0Tq
H4guEZisNIp1YTySb+rP3YXvMEImYdalcsii5rkCgYEAimnWJ5aFN3TDt3h76CL3
nRQegnzekJBjXZfcrHdExkgNChWjiz+WU/FW/Z87xMxtfIEwwzzIQHxbKZhgzO/U
p2eXdqH59DvauggbiS3h4p9k2kxWTocztarvdftMW0ncmA4yCKiUQEmWD784JCyx
OupNNfr2rgViWggVBEtJUIg=
-----END PRIVATE KEY-----""")

rsa1 = RSA.importKey("""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDbfWw2tfpbGVCl
+zLy7pVH2vDgfiVj3d+ykCZd5+MOFCFgI8z5LKkG8iBv/D1/wAaQTBSUNDF9kIKX
PvYYC5L2OuWyqD0ulIxn48kA7QENaKywkIm3LIQ1b/1VU+kksDRJJ5i5NgnzhYMB
yOxvRP75X3tNeVKKr2y9e3XosPEJAmNFe/07VRMGQOkYZmadHjEuJBP4/Hoo6oCy
slwAXQQlqOLloF8dVB2tdDCCarw8Sx+e+naJAItnaIM8uUZtFqF0V6KBddPgvpS+
OlsWv/0g28Nvb69CRGXvOUdW1QAxHhfmyZbacccfljJOLVw68wWw36g8bGAEalKp
gLGY/Ag3AgMBAAECggEADbfJC6JUA12RrM4GYSiIK/WDGITJ0XQMhxx7SWM0zax0
aY3TQb+I0OZRIK6jKVjXEC2xG5InhbGCd/F3cAlJJhqIQKJDMKYYIGYcKfKmHjBs
mpxt/wTJPo3BR5P2/lQE8I2I/gpilNXDWlk0bb/iL7PIAQ+UGRbdtPoCZIiqh+WA
qElaJ4LHXgKBXUpozfEtUa383IcwsQdB1BSwMOnJ5YFrplhx6fTgJ6noFB4eLp7h
SCSR2018r11UAANqWbc7a40TtLpWUmh3AExCeQACI1RloTSCRWYsXrxFMH6ZGDvE
K+Q9LS+jtkPCtOrbr+j8FU0Dgxh/5P0I2xR4hcgAAQKBgQDkcnwcaWRZv0uFxAtj
q3pVelWuu3uapwroO9asmeWsmL3LQeW22X5CNy1gYOlhyG6FqfMLOmzhCicFYX45
6EiDJpyX/LVcSDmzmTDwI25uEunhyhVATJWqwaITdLrJf8KDqqO8bvUHc/wB//2T
OTWpUB542DZJ2A8aServjR6ErwKBgQD19l+5xCHLOldtV56hbAQnhhl8lUAL/mBq
wXNrDNeqmDYFJ3kkHWk5raXUQR41qAubhKnLUJ4qj6FIBcRmsrTMITMWZ9/GzJhK
mNU+nync2IlSS7g3Vyee3wz1Fd2dRA3NwZ9JVK+xTSKgw1a/VXKcfC+iYnXmVIxa
3cCIZ9Um+QKBgQDE34Dj/1OzIG+WbPgfwiTgS1hSCFKiWfjFYORFxS8wykUuSLEO
Hmt35xNc7sfSNChDWs4QzB4O5m/wbC+a+fqbxAfJ18f4KmpHw+pv2SkPBY+3vS8J
Rbbp/IuP1tYuVsMsMz9+YeUasjLpClLesLv1GQ3ZuQM4KlIBptgn7+bwEwKBgQC1
ZDk8etShWClZziCC03JM46ywIDHXpoXctUY1UIdMnGxaaL4CUF5l1xZQ7qUk1QWa
b7/43T+IC9zZjMdHJcwILwPKJlj197TobsX1JNRutpKvSoBU78WceMrJhJKnhKTZ
dU3PetEHZOeAwA6dlJqtpThL/WkNsJTB/oAbGNgtoQKBgG4ytUXXwp61VHm/3Pon
9d6z5o02AQVCppJRcJwehbAm14813G/jPfjwM+KZ2ikhs+eW1peWhBrCo+M5/u5T
bxeDm9cbLMewkYNIdvUxtaBb+fJtIBAngAL2HEhqBdUFoQI+lr+F802UO2aM8Sg+
n82S/+EJZomQ7hhO7qnLtxkI
-----END PRIVATE KEY-----""")

pkcs0 = PKCS1_v1_5.new(rsa0)
pkcs1 = PKCS1_v1_5.new(rsa1)

def parse(mid, dstport, data, key):
    while len(data) >= 20:
        plen, iv = struct.unpack(">I16s", data[:20])
        assert plen % 16 == 0
        if len(data) < 20 + plen:
            break
        pkt = data[20:20+plen]
        del data[:20+plen]
        cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
        r = unpad(cipher.decrypt(pkt), 16)
        print(mid, dstport, r.hex(), sep="\t")

class MuxStream:
    def __init__(self):
        self.c2s = bytearray()
        self.s2c = bytearray()
        self.key = None

    def add(self, mid, dstport, data):
        if dstport == 8888:
            self.c2s += data
        else:
            self.s2c += data

        if self.key is None and len(self.c2s) >= 290 and len(self.s2c) >= 290:
            kex0 = self.s2c[2:258]
            kex1 = self.c2s[2:258]
            key0 = pkcs0.decrypt(kex0, sentinel)
            assert key0 != sentinel
            key1 = pkcs1.decrypt(kex1, sentinel)
            assert key1 != sentinel
            self.key = bytes([a^b for a,b in zip(key0, key1)])
            assert hashlib.sha256(self.key).digest() == self.s2c[258:290]
            assert hashlib.sha256(self.key).digest() == self.c2s[258:290]
            self.s2c = self.s2c[290:]
            self.c2s = self.c2s[290:]

        if self.key is not None:
            if dstport == 8888:
                parse(mid, dstport, self.c2s, self.key)
            else:
                parse(mid, dstport, self.s2c, self.key)

streams = defaultdict(MuxStream)

for row in open("dump2.txt"):
    stream, dstport, cmd, mid, data = row.split("\t")
    dstport = int(dstport)
    cmd = int(cmd)
    mid = int(mid)
    data = bytes.fromhex(data)
    if cmd == 1:
        streams[mid].add(mid, dstport, data)
```

Running this, we get the final decrypted dump ([`dump3.txt`](dump3.txt)):

```
0	8888	050100
0	50671	0500
1	8888	050100
1	50671	0500
0	8888	050100030f3139322e3136382e3231392e3233331f40
1	8888	050100030f3139322e3136382e3231392e3233331f40
0	50671	05000001c0a8db01c5f5
0	8888	474554202f20485454502f312e310d0a486f73743a203139322e3136382e3231392e3233333a383030300d0a436f6e6e656374696f6e3a206b6565702d616c6976650d0a507261676d613a206e6f2d63616368650d0a43616368652d436f6e74726f6c3a206e6f2d63616368650d0a557067726164652d496e7365637572652d52657175657374733a20310d0a557365722d4167656e743a204d6f7a696c6c612f352e30202857696e646f7773204e542031302e303b2057696e36343b2078363429204170706c655765624b69742f3533372e333620284b48544d4c2c206c696b65204765636b6f29204368726f6d652f3130382e302e302e30205361666172692f3533372e33360d0a4163636570743a20746578742f68746d6c2c6170706c69636174696f6e2f7868746d6c2b786d6c2c6170706c69636174696f6e2f786d6c3b713d302e392c696d6167652f617669662c696d6167652f776562702c696d6167652f61706e672c2a2f2a3b713d302e382c6170706c69636174696f6e2f7369676e65642d65786368616e67653b763d62333b713d302e390d0a4163636570742d456e636f64696e673a20677a69702c206465666c6174650d0a4163636570742d4c616e67756167653a207a682d434e2c7a683b713d302e392c656e2d55533b713d302e382c656e3b713d302e370d0a0d0a
1	50671	05000001c0a8db01c5f6
0	50671	485454502f312e3020323030204f4b0d0a5365727665723a2053696d706c65485454502f302e3620507974686f6e2f332e362e390d0a446174653a204672692c203036204a616e20323032332031383a31363a343720474d540d0a436f6e74656e742d747970653a20746578742f68746d6c3b20636861727365743d7574662d380d0a436f6e74656e742d4c656e6774683a203333380d0a0d0a3c21444f43545950452048544d4c205055424c494320222d2f2f5733432f2f4454442048544d4c20342e30312f2f454e222022687474703a2f2f7777772e77332e6f72672f54522f68746d6c342f7374726963742e647464223e0a3c68746d6c3e0a3c686561643e0a3c6d65746120687474702d65717569763d22436f6e74656e742d547970652220636f6e74656e743d22746578742f68746d6c3b20636861727365743d7574662d38223e0a3c7469746c653e4469726563746f7279206c697374696e6720666f72202f3c2f7469746c653e0a3c2f686561643e0a3c626f64793e0a3c68313e4469726563746f7279206c697374696e6720666f72202f3c2f68313e0a3c68723e0a3c756c3e0a3c6c693e3c6120687265663d22666c61672e747874223e666c61672e7478743c2f613e3c2f6c693e0a3c2f756c3e0a3c68723e0a3c2f626f64793e0a3c2f68746d6c3e0a
1	8888	474554202f66617669636f6e2e69636f20485454502f312e310d0a486f73743a203139322e3136382e3231392e3233333a383030300d0a436f6e6e656374696f6e3a206b6565702d616c6976650d0a507261676d613a206e6f2d63616368650d0a43616368652d436f6e74726f6c3a206e6f2d63616368650d0a557365722d4167656e743a204d6f7a696c6c612f352e30202857696e646f7773204e542031302e303b2057696e36343b2078363429204170706c655765624b69742f3533372e333620284b48544d4c2c206c696b65204765636b6f29204368726f6d652f3130382e302e302e30205361666172692f3533372e33360d0a4163636570743a20696d6167652f617669662c696d6167652f776562702c696d6167652f61706e672c696d6167652f7376672b786d6c2c696d6167652f2a2c2a2f2a3b713d302e380d0a526566657265723a20687474703a2f2f3139322e3136382e3231392e3233333a383030302f0d0a4163636570742d456e636f64696e673a20677a69702c206465666c6174650d0a4163636570742d4c616e67756167653a207a682d434e2c7a683b713d302e392c656e2d55533b713d302e382c656e3b713d302e370d0a0d0a
1	50671	485454502f312e30203430342046696c65206e6f7420666f756e640d0a5365727665723a2053696d706c65485454502f302e3620507974686f6e2f332e362e390d0a446174653a204672692c203036204a616e20323032332031383a31363a343720474d540d0a436f6e6e656374696f6e3a20636c6f73650d0a436f6e74656e742d547970653a20746578742f68746d6c3b636861727365743d7574662d380d0a436f6e74656e742d4c656e6774683a203436390d0a0d0a3c21444f43545950452048544d4c205055424c494320222d2f2f5733432f2f4454442048544d4c20342e30312f2f454e220a202020202020202022687474703a2f2f7777772e77332e6f72672f54522f68746d6c342f7374726963742e647464223e0a3c68746d6c3e0a202020203c686561643e0a20202020202020203c6d65746120687474702d65717569763d22436f6e74656e742d547970652220636f6e74656e743d22746578742f68746d6c3b636861727365743d7574662d38223e0a20202020202020203c7469746c653e4572726f7220726573706f6e73653c2f7469746c653e0a202020203c2f686561643e0a202020203c626f64793e0a20202020202020203c68313e4572726f7220726573706f6e73653c2f68313e0a20202020202020203c703e4572726f7220636f64653a203430343c2f703e0a20202020202020203c703e4d6573736167653a2046696c65206e6f7420666f756e642e3c2f703e0a20202020202020203c703e4572726f7220636f6465206578706c616e6174696f6e3a20485454505374617475732e4e4f545f464f554e44202d204e6f7468696e67206d6174636865732074686520676976656e205552492e3c2f703e0a202020203c2f626f64793e0a3c2f68746d6c3e0a
3	8888	050100
3	50671	0500
3	8888	050100030f3139322e3136382e3231392e3233331f40
3	50671	05000001c0a8db01c5f9
3	8888	474554202f666c61672e74787420485454502f312e310d0a486f73743a203139322e3136382e3231392e3233333a383030300d0a436f6e6e656374696f6e3a206b6565702d616c6976650d0a557067726164652d496e7365637572652d52657175657374733a20310d0a557365722d4167656e743a204d6f7a696c6c612f352e30202857696e646f7773204e542031302e303b2057696e36343b2078363429204170706c655765624b69742f3533372e333620284b48544d4c2c206c696b65204765636b6f29204368726f6d652f3130382e302e302e30205361666172692f3533372e33360d0a4163636570743a20746578742f68746d6c2c6170706c69636174696f6e2f7868746d6c2b786d6c2c6170706c69636174696f6e2f786d6c3b713d302e392c696d6167652f617669662c696d6167652f776562702c696d6167652f61706e672c2a2f2a3b713d302e382c6170706c69636174696f6e2f7369676e65642d65786368616e67653b763d62333b713d302e390d0a526566657265723a20687474703a2f2f3139322e3136382e3231392e3233333a383030302f0d0a4163636570742d456e636f64696e673a20677a69702c206465666c6174650d0a4163636570742d4c616e67756167653a207a682d434e2c7a683b713d302e392c656e2d55533b713d302e382c656e3b713d302e370d0a0d0a
3	50671	485454502f312e3020323030204f4b0d0a5365727665723a2053696d706c65485454502f302e3620507974686f6e2f332e362e390d0a446174653a204672692c203036204a616e20323032332031383a31363a343920474d540d0a436f6e74656e742d747970653a20746578742f706c61696e0d0a436f6e74656e742d4c656e6774683a2033380d0a4c6173742d4d6f6469666965643a204672692c203036204a616e20323032332031383a31353a353220474d540d0a0d0a72776374667b6c3166655f31735f73683072745f444f305f6e6f745f7573335f727573747d0a
2	8888	050100
2	50671	0500
2	8888	050100030f3139322e3136382e3231392e3233331f40
2	50671	05000001c0a8db01c5fa
```

This is a set of HTTP requests and responses. One of the final messages contains our flag:

`rwctf{l1fe_1s_sh0rt_DO0_not_us3_rust}`
