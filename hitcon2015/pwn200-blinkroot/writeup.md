# blinkroot (pwn 200)

binary reads 1024 bytes, then closes stdin,stderr,stdout

then there is a MOVAPS to copy 8 bytes of input to a controllable address

so the destination address must be aligned properly

i chose to overwrite pointer to link_map, and provide a fake link_map that

returns the address of system when trying to resolve the address of puts

exploit does a reverse tcp, command length ended up being constrained to

under 24 bytes, so we had a short domain name listening on a 1 digit port
