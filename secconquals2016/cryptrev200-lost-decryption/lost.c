// Author: Adam Van Prooyen [@docileninja, @scienceman]
// Solution for SECCON 'Lost Decryption'; requires key.bin, flag.enc, and
// libencrypt.so in the same directory.

#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdint.h>

#define ROUNDS 14

uint8_t *libencrypt;
uint64_t (* f)(uint64_t, uint64_t); // round function for the fiestel network

uint64_t keys[ROUNDS]; // key schedule for decryption (reverse of encryption schedule)
uint64_t c = 0x9104F95DE694DC50; // constant from binary for generating next key

void swap(uint64_t *a, uint64_t *b) {
	uint64_t tmp = *a;
	*a = *b;
	*b = tmp;
}

void load_f() {
	struct stat st;
	int fd;

	fd = open("libencrypt.so", O_RDWR);
	fstat(fd, &st);

	libencrypt = mmap(NULL, st.st_size, PROT_EXEC, MAP_PRIVATE, fd, 0);
	f = (uint64_t (*)(uint64_t, uint64_t)) &libencrypt[0x700];
}

void load_keys(uint64_t *k_L1, uint64_t *k_R1) {
	int fd;
	char buf[16];

	fd = open("key.bin", O_RDONLY);
	read(fd, buf, 16);

	*k_L1 = *(uint64_t *) buf;
	*k_R1 = *((uint64_t *) buf + 1);
}

void load_ct(char ct[48]) {
	int fd;

	fd = open("flag.enc", O_RDONLY);
	
	read(fd, ct, 48);
}

void gen_keys(uint64_t k_L, uint64_t k_R) {
	int i;

	for (i = 0; i < ROUNDS; i++) {
		keys[ROUNDS - i - 1] = k_R;
		k_R = f(k_R, c);
		swap(&k_L, &k_R);
	}
}

void decrypt(char *ct) {
	uint64_t k_n, L, R;
	int i;

	L = *(uint64_t *) ct;
	R = *((uint64_t *) ct + 1);
	for (i = 0; i < ROUNDS; i++) {
		k_n = keys[i];
		L ^= f(R, k_n);
		swap(&L, &R);
	}
	*(uint64_t *) ct = L;
	*((uint64_t *) ct + 1) = R;
}

int main() {
	int i;
	uint64_t k_L1, k_R1;
	char ct[49];

	load_f();
	load_ct(ct);
	load_keys(&k_L1, &k_R1);
	gen_keys(k_L1, k_R1);

	printf("k_L1: %016llx k_R1: %016llx\n", k_L1, k_R1);
	printf("keys:\n");
	for (i = 0; i < ROUNDS; i++) {
		printf("  %2d: %016llx\n", i+1, keys[i]);
	}

	for (i = 0; i < 3; i++) {
		decrypt(&ct[i * 16]);
	}
	ct[48] = 0;
	printf("Flag: %s\n", ct);

	return 0;
}