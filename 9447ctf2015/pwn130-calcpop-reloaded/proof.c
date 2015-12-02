/*
 * gcc -O3 -o proof proof.c $(pkg-config --cflags --libs openssl)
 */
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <openssl/bio.h>
#include <openssl/evp.h>

int main(int argc, char **argv) {
    const char *target = "\x00\x00\x00";
    unsigned int i;
    char data[1024];
    unsigned char hash[20];
    do {
        ++i;
        snprintf(data, sizeof(data), "%s%08d", argv[1], i);
        SHA1((char *) &data, strlen(data), hash);
    } while (memcmp(target, &hash[17], 3) != 0);
    
    puts(data);
    return 0;
}
