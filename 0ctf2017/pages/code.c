#include <stdint.h>

static uint64_t run_once(void *addr) {
  uint64_t start_low, start_high, start_core;

  asm volatile("mfence");
  asm volatile("cpuid" ::"a"(0) : "ebx", "ecx", "edx");
  asm volatile("rdtscp" : "=a"(start_low), "=d"(start_high), "=c"(start_core));
  asm volatile("prefetcht2 (%%rdi);" : : "D"(addr));

  uint64_t end_low, end_high, end_core;
  asm volatile("rdtscp" : "=a"(end_low), "=d"(end_high), "=c"(end_core));
  asm volatile("cpuid" ::"a"(0) : "ebx", "ecx", "edx");
  asm volatile("mfence");

  if (start_core != end_core) {
    return 0;
  }

  const uint64_t start = (start_high << 32) | start_low;
  const uint64_t end = (end_high << 32) | end_low;
  return end - start;
}

static uint64_t timeit(void *addr) {
  uint64_t best = UINT64_MAX;

  int i = 0;
  while (i < 5000) {
    uint64_t time = run_once(addr);
    if (time == 0) {
      continue;
    }
    if (time < best) {
      best = time;
    }
    ++i;
  }

  return best;
}

void entry(void) {
  int i;
  char *out = (char *) 0x300000000;
  uint64_t* debug = (uint64_t*)out;
  for (i = 0; i < 64; ++i) {
    char *page0 = (char *)0x200000000 + 2 * i * 0x1000;
    char *page1 = page0 + 0x1000;
    uint64_t time0 = timeit(page0);
    uint64_t time1 = timeit(page1);
    if (time1 < time0) {
      out[i] = 1;
    }
  }

  asm("int3");
}
