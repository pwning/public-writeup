## Good_Crypto - Programming 500 Problem

The given file is a packet dump encrypted with WEP (as the "WiFi" icon in the problem hints at). A few seconds with `wepcrack` solves that nicely, and gives us the WEP key `A4:3D:F6:F3:74`.

Inspecting the pcap, we can see some communication to a local 192.168.* address, presumably some kind of router. One of the pages downloaded contains a form asking for the "WEP Passphrase", and a short JavaScript snippet that checks if the passphrase is alphabetic, computes the SHA-1 hash of the passphrase, and checks if it starts with `ff7b948953ac`. This passphrase is our flag.

So now we have to figure out what the passphrase is, given a WEP key derived from it and a partial SHA-1 hash.

WEP keys are derived from passphrases using a de-facto industry standard method, which basically consists of xoring four-byte blocks of the passphrase together, and using the resulting 32-bit number as a seed for a linear-congruential PRNG. It's pretty easy to obtain the seed by bruteforcing it, but it turns out there are many seeds which can generate the observed key. All the valid seeds are of the form `0xXX12766b` where XX is any byte.

Since the seed is obtained by xoring four-byte blocks of the passphrase together, the seed is a restriction on the possible passphrases. Since the passphrase is alphabetic, we can infer that the passphrase is 10 characters long from the seed (since all alphabetic characters have bit 0x40 set). So we're looking to bruteforce a 10-character alphabetic password, with 3 restrictions - it's basically 7 characters, and that seems plausible given modern hardware.

We coded a simple wordlist generator and piped it into John the Ripper (modified to only check the first 6 bytes of the SHA-1 hash). An hour later, the bruteforce was done and we got the flag: `cgwepkeyxz`.