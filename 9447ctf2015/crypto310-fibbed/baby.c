// g++ -std=c++11 ./baby.c -o baby

#include "stdlib.h"
#include <unordered_map>

typedef std::unordered_map<uint64_t, uint64_t> my_map;

unsigned long p = 981725946171163877;
unsigned long order = 1963451892342327757;
unsigned long m = 1401232276;


typedef struct tup_ {
  unsigned long f0;
  unsigned long f1;
} tup;

//number for which we want to take the discrete log
tup beta = {58449491987662952, 704965025359609904};

//F_{order - m}
tup alphaminm = {939787032033804662, 494201146526770439};


void mult(tup* t1, tup* t2, tup* out) {
  __uint128_t a00, a01, a11;
  __uint128_t b00, b01, b11;
  a00 = t1->f0;
  a01 = t1->f1;
  a11 = (a00+a01)%p;
  b00 = t2->f0;
  b01 = t2->f1;
  b11 = (b00+b01)%p;

  out->f0 = ((a00*b00)%p + (a01*b01)%p)%p;
  out->f1 = ((a00*b01)%p + (a01*b11)%p)%p;
}

void insert(unsigned int* hashmap, unsigned long hash, unsigned int value) {
  if (hashmap[hash]) {
  //already stuff here, grow things

  }
  else {
    //empty, add something
    hashmap[hash] = value;
  }
}

int main(int argc, char** argv) {
  unsigned long mm0, mm1, mm2;
  unsigned int i;
  mm0 = 0;
  mm1 = 1;

  my_map map;

  for (i = 1; i < m; i++) {
    mm2 = (mm0 + mm1)%p;
    map[mm1^mm2] = i;
    mm0 = mm1;
    mm1 = mm2;
    if (i % 10000000 == 0) {
      printf("table filling %d/%ld\n", i, m);
    }
  }

  tup gamma;
  gamma.f0 = beta.f0;
  gamma.f1 = beta.f1;
  for (i = 0; i < m; i++) {
    if (map.count(gamma.f0^gamma.f1)) {
      printf("FOUND!!!!! %d %ld %ld\n", i, map[gamma.f0^gamma.f1], i*m + (uint64_t)map[gamma.f0^gamma.f1] + 1);
    }
    mult(&alphaminm, &gamma, &gamma);
    if (i % 10000000 == 0) {
      printf("table searching %d/%ld\n", i, m);
    }
  }
  return 0;
}
