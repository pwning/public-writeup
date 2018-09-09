char t1[] = {1, 0, 5, 3, 14, 2, 15, 7, 13, 10, 9, 11, 12, 8, 4, 6};

char munge0(char x) {
    char y = x & 0x55;
    y |= (x & 0x8) << 4;
    y |= (x & 0x2) << 4;
    y ^= (x & 0x80) >> 4;
    y ^= (x & 0x20) >> 4;
    return y;
}

char munge1(char x) {
    char y;
    y = (x & 2) << 5;
    y |= (x & 0x40) << 1;
    y ^= (x & 1) << 5;
    y ^= (x & 0x80) >> 3;
    y ^= (x & 4) << 1;
    y ^= (x & 0x20) >> 3;
    y ^= (x & 0x10) >> 3;
    y ^= (x & 0x8) >> 3;
    return y;
}

char munge1_1(char x) {
    char y;
    y = (x & 0x80) >> 1;
    y ^= (x & 0x10) << 3;
    y ^= (x & 4) << 3;
    y ^= (x & 2) << 3;
    y ^= (x & 1) << 3;
    y ^= (x & 8) >> 1;
    y ^= (x & 0x40) >> 5;
    y ^= (x & 0x20) >> 5;
    return y;
}

char munge2(char x) {
    char y;
    y = (x & 0x38) << 2;
    y ^= (x & 0x40) >> 2;
    y ^= (x & 2) << 2;
    y ^= (x & 1) << 2;
    y ^= (x & 0x80) >> 6;
    y ^= (x & 0x4) >> 2;
    return y;
}

char munge2_1(char x) {
    char y;
    y = (x & 0x10) << 2;
    y |= (x & 2) << 6;
    y ^= (x & 0x80) >> 2;
    y ^= (x & 0x40) >> 2;
    y ^= (x & 0x20) >> 2;
    y ^= (x & 1) << 2;
    y ^= (x & 8) >> 2;
    y ^= (x & 4) >> 2;
    return y;
}

char munge3(char x) {
    char y;
    y = (x & 8) << 3;
    y ^= (x & 0x40) >> 1;
    y ^= (x & 1) << 7;
    y ^= (x & 0x20) >> 1;
    y ^= (x & 0x10) >> 1;
    y ^= (x & 0x80) >> 5;
    y ^= (x & 4) >> 1;
    y ^= (x & 2) >> 1;
    return y;
}

char munge3_1(char x) {
    char y;
    y = (x & 4) << 5;
    y ^= (x & 0x20) << 1;
    y ^= (x & 0x80) >> 7; // ?
    y ^= (x & 0x10) << 1;
    y ^= (x & 8) << 1;
    y ^= (x & 0x40) >> 3;
    y ^= (x & 2) << 1;
    y ^= (x & 1) << 1;
    return y;
}

static inline __attribute__((always_inline)) char apply_t1(char x) {
    return (t1[(x & 0xf0) >> 4] * 16) ^ t1[x & 0xf];
}

char __attribute__((noinline)) encrypt_t1_1(int round, char x) {
    if((round % 4) == 0) {
        x = munge0(x);
        x = apply_t1(x);
        return munge0(x);
    } else if((round % 4) == 1) {
        x = munge1(x);
        x = apply_t1(x);
        return munge1_1(x);
    } else if((round % 4) == 2) {
        x = munge2(x);
        x = apply_t1(x);
        return munge2_1(x);
    } else if((round % 4) == 3) {
        x = munge3(x);
        x = apply_t1(x);
        return munge3_1(x);
    }
}
