/* 
 * SHA-1 hash in C and x86 assembly
 * 
 * Copyright (c) 2016 Project Nayuki
 * https://www.nayuki.io/page/fast-sha1-hash-implementation-in-x86-assembly
 * 
 * (MIT License)
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 * - The above copyright notice and this permission notice shall be included in
 *   all copies or substantial portions of the Software.
 * - The Software is provided "as is", without warranty of any kind, express or
 *   implied, including but not limited to the warranties of merchantability,
 *   fitness for a particular purpose and noninfringement. In no event shall the
 *   authors or copyright holders be liable for any claim, damages or other
 *   liability, whether in an action of contract, tort or otherwise, arising from,
 *   out of or in connection with the Software or the use or other dealings in the
 *   Software.
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


/* Function prototypes */
void sha1_hash(const uint8_t *message, uint32_t len, uint32_t hash[5]);

// Link this program with an external C or x86 compression function
extern void sha1_compress(uint32_t state[5], const uint8_t block[64]);


/* Main program */

int main(int argc, char **argv) {
	uint8_t block[32];
	uint8_t hash[20];

	memset(block, 0, sizeof(block));
	unsigned int prefix = fread(block, 1, sizeof(block), stdin);

	for (unsigned long x = 0;; x++)
	{
		*(unsigned long *)&block[prefix] = x;
		sha1_hash(block, sizeof(block), (void *)hash);
		if (hash[3] == 0 && hash[1] == 0 && hash[2] == 0) {
			fwrite(block, 1, sizeof(block), stdout);
			return 0;
		}
	}

	return 1;
}


/* Full message hasher */

void sha1_hash(const uint8_t *message, uint32_t len, uint32_t hash[5]) {
    hash[0] = UINT32_C(0x67452301);
    hash[1] = UINT32_C(0xEFCDAB89);
    hash[2] = UINT32_C(0x98BADCFE);
    hash[3] = UINT32_C(0x10325476);
    hash[4] = UINT32_C(0xC3D2E1F0);
    
    uint32_t i;
    for (i = 0; len - i >= 64; i += 64)
        sha1_compress(hash, message + i);
    
    uint8_t block[64];
    uint32_t rem = len - i;
    memcpy(block, message + i, rem);
    
    block[rem] = 0x80;
    rem++;
    if (64 - rem >= 8)
        memset(block + rem, 0, 56 - rem);
    else {
        memset(block + rem, 0, 64 - rem);
        sha1_compress(hash, block);
        memset(block, 0, 56);
    }
    
    uint64_t longLen = ((uint64_t)len) << 3;
    for (i = 0; i < 8; i++)
        block[64 - 1 - i] = (uint8_t)(longLen >> (i * 8));
    sha1_compress(hash, block);
}
