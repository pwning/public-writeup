/* sha1.c - SHA1 hash function
 * Copyright (C) 1998, 2001, 2002, 2003, 2008 Free Software Foundation, Inc.
 *
 * This file is part of Libgcrypt.
 *
 * Libgcrypt is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation; either version 2.1 of
 * the License, or (at your option) any later version.
 *
 * Libgcrypt is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program; if not, see <http://www.gnu.org/licenses/>.
 */


/*  Test vectors:
 *
 *  "abc"
 *  A999 3E36 4706 816A BA3E  2571 7850 C26C 9CD0 D89D
 *
 *  "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
 *  8498 3E44 1C3B D26E BAAE  4AA1 F951 29E5 E546 70F1
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef HAVE_STDINT_H
# include <stdint.h>
#endif

typedef struct
{
	uint32_t          h0,h1,h2,h3,h4;
} SHA1_CONTEXT;

static inline uint32_t rol(uint32_t x, int n)
{
	return ( (x << (n&(32-1))) | (x >> ((32-n)&(32-1))) );
}

static inline uint32_t buf_get_be32(const void *_buf)
{
	const unsigned char *in = _buf;
	return ((uint32_t)in[0] << 24) | ((uint32_t)in[1] << 16) | \
	((uint32_t)in[2] << 8) | (uint32_t)in[3];
}

/* A macro to test whether P is properly aligned for an u32 type.
   Note that config.h provides a suitable replacement for uintptr_t if
   it does not exist in stdint.h.  */
/* #if __GNUC__ >= 2 */
/* # define U32_ALIGNED_P(p) (!(((uintptr_t)p) % __alignof__ (u32))) */
/* #else */
/* # define U32_ALIGNED_P(p) (!(((uintptr_t)p) % sizeof (u32))) */
/* #endif */


static unsigned int
transform (void *c, const unsigned char *data, size_t nblks);


static void
sha1_init (void *context, unsigned int flags)
{
  SHA1_CONTEXT *hd = context;

  (void)flags;

  hd->h0 = 0x67452301;
  hd->h1 = 0xefcdab89;
  hd->h2 = 0x98badcfe;
  hd->h3 = 0x10325476;
  hd->h4 = 0xc3d2e1f0;
}

/*
 * Initialize the context HD. This is used to prepare the use of
 * _gcry_sha1_mixblock.  WARNING: This is a special purpose function
 * for exclusive use by random-csprng.c.
 */
void
_gcry_sha1_mixblock_init (SHA1_CONTEXT *hd)
{
  sha1_init (hd, 0);
}


/* Round function macros. */
#define K1  0x5A827999L
#define K2  0x6ED9EBA1L
#define K3  0x8F1BBCDCL
#define K4  0xCA62C1D6L
#define F1(x,y,z)   ( z ^ ( x & ( y ^ z ) ) )
#define F2(x,y,z)   ( x ^ y ^ z )
#define F3(x,y,z)   ( ( x & y ) | ( z & ( x | y ) ) )
#define F4(x,y,z)   ( x ^ y ^ z )
#define M(i) ( tm =    x[ i    &0x0f]  \
                     ^ x[(i-14)&0x0f]  \
	 	     ^ x[(i-8) &0x0f]  \
                     ^ x[(i-3) &0x0f], \
                     (x[i&0x0f] = rol(tm, 1)))
#define R(a,b,c,d,e,f,k,m)  do { e += rol( a, 5 )     \
	                              + f( b, c, d )  \
		 		      + k	      \
			 	      + m;	      \
				 b = rol( b, 30 );    \
			       } while(0)


/*
 * Transform NBLOCKS of each 64 bytes (16 32-bit words) at DATA.
 */
static unsigned int
transform_blk (void *ctx, const unsigned char *data)
{
  SHA1_CONTEXT *hd = ctx;
  const uint32_t *idata = (const void *)data;
  register uint32_t a, b, c, d, e; /* Local copies of the chaining variables.  */
  register uint32_t tm;            /* Helper.  */
  uint32_t x[16];                  /* The array we work on. */

#define I(i) (x[i] = buf_get_be32(idata + i))

      /* Get the values of the chaining variables. */
      a = hd->h0;
      b = hd->h1;
      c = hd->h2;
      d = hd->h3;
      e = hd->h4;

      /* Transform. */
      R( a, b, c, d, e, F1, K1, I( 0) );
      R( e, a, b, c, d, F1, K1, I( 1) );
      R( d, e, a, b, c, F1, K1, I( 2) );
      R( c, d, e, a, b, F1, K1, I( 3) );
      R( b, c, d, e, a, F1, K1, I( 4) );
      R( a, b, c, d, e, F1, K1, I( 5) );
      R( e, a, b, c, d, F1, K1, I( 6) );
      R( d, e, a, b, c, F1, K1, I( 7) );
      R( c, d, e, a, b, F1, K1, I( 8) );
      R( b, c, d, e, a, F1, K1, I( 9) );
      R( a, b, c, d, e, F1, K1, I(10) );
      R( e, a, b, c, d, F1, K1, I(11) );
      R( d, e, a, b, c, F1, K1, I(12) );
      R( c, d, e, a, b, F1, K1, I(13) );
      R( b, c, d, e, a, F1, K1, I(14) );
      R( a, b, c, d, e, F1, K1, I(15) );
      R( e, a, b, c, d, F1, K1, M(16) );
      R( d, e, a, b, c, F1, K1, M(17) );
      R( c, d, e, a, b, F1, K1, M(18) );
      R( b, c, d, e, a, F1, K1, M(19) );
      R( a, b, c, d, e, F2, K2, M(20) );
      R( e, a, b, c, d, F2, K2, M(21) );
      R( d, e, a, b, c, F2, K2, M(22) );
      R( c, d, e, a, b, F2, K2, M(23) );
      R( b, c, d, e, a, F2, K2, M(24) );
      R( a, b, c, d, e, F2, K2, M(25) );
      R( e, a, b, c, d, F2, K2, M(26) );
      R( d, e, a, b, c, F2, K2, M(27) );
      R( c, d, e, a, b, F2, K2, M(28) );
      R( b, c, d, e, a, F2, K2, M(29) );
      R( a, b, c, d, e, F2, K2, M(30) );
      R( e, a, b, c, d, F2, K2, M(31) );
      R( d, e, a, b, c, F2, K2, M(32) );
      R( c, d, e, a, b, F2, K2, M(33) );
      R( b, c, d, e, a, F2, K2, M(34) );
      R( a, b, c, d, e, F2, K2, M(35) );
      R( e, a, b, c, d, F2, K2, M(36) );
      R( d, e, a, b, c, F2, K2, M(37) );
      R( c, d, e, a, b, F2, K2, M(38) );
      R( b, c, d, e, a, F2, K2, M(39) );
      R( a, b, c, d, e, F3, K3, M(40) );
      R( e, a, b, c, d, F3, K3, M(41) );
      R( d, e, a, b, c, F3, K3, M(42) );
      R( c, d, e, a, b, F3, K3, M(43) );
      R( b, c, d, e, a, F3, K3, M(44) );
      R( a, b, c, d, e, F3, K3, M(45) );
      R( e, a, b, c, d, F3, K3, M(46) );
      R( d, e, a, b, c, F3, K3, M(47) );
      R( c, d, e, a, b, F3, K3, M(48) );
      R( b, c, d, e, a, F3, K3, M(49) );
      R( a, b, c, d, e, F3, K3, M(50) );
      R( e, a, b, c, d, F3, K3, M(51) );
      R( d, e, a, b, c, F3, K3, M(52) );
      R( c, d, e, a, b, F3, K3, M(53) );
      R( b, c, d, e, a, F3, K3, M(54) );
      R( a, b, c, d, e, F3, K3, M(55) );
      R( e, a, b, c, d, F3, K3, M(56) );
      R( d, e, a, b, c, F3, K3, M(57) );
      R( c, d, e, a, b, F3, K3, M(58) );
      R( b, c, d, e, a, F3, K3, M(59) );
      R( a, b, c, d, e, F4, K4, M(60) );
      R( e, a, b, c, d, F4, K4, M(61) );
      R( d, e, a, b, c, F4, K4, M(62) );
      R( c, d, e, a, b, F4, K4, M(63) );
      R( b, c, d, e, a, F4, K4, M(64) );
      R( a, b, c, d, e, F4, K4, M(65) );
      R( e, a, b, c, d, F4, K4, M(66) );
      R( d, e, a, b, c, F4, K4, M(67) );
      R( c, d, e, a, b, F4, K4, M(68) );
      R( b, c, d, e, a, F4, K4, M(69) );
      R( a, b, c, d, e, F4, K4, M(70) );
      R( e, a, b, c, d, F4, K4, M(71) );
      R( d, e, a, b, c, F4, K4, M(72) );
      R( c, d, e, a, b, F4, K4, M(73) );
      R( b, c, d, e, a, F4, K4, M(74) );
      R( a, b, c, d, e, F4, K4, M(75) );
      R( e, a, b, c, d, F4, K4, M(76) );
      R( d, e, a, b, c, F4, K4, M(77) );
      R( c, d, e, a, b, F4, K4, M(78) );
      R( b, c, d, e, a, F4, K4, M(79) );


      /* Update the chaining variables. */
      hd->h0 += a;
      hd->h1 += b;
      hd->h2 += c;
      hd->h3 += d;
      hd->h4 += e;

  return /* burn_stack */ 88+4*sizeof(void*);
}

static unsigned int
transform (void *ctx, const unsigned char *data, size_t nblks)
{
  SHA1_CONTEXT *hd = ctx;
  unsigned int burn;
  do
    {
      burn = transform_blk (hd, data);
      data += 64;
    }
  while (--nblks);

  return burn;
}


/*
 * Apply the SHA-1 transform function on the buffer BLOCKOF64BYTE
 * which must have a length 64 bytes.  BLOCKOF64BYTE must be 32-bit
 * aligned.  Updates the 20 bytes in BLOCKOF64BYTE with its mixed
 * content.  Returns the number of bytes which should be burned on the
 * stack.  You need to use _gcry_sha1_mixblock_init to initialize the
 * context.
 * WARNING: This is a special purpose function for exclusive use by
 * random-csprng.c.
 */
unsigned int
_gcry_sha1_mixblock (SHA1_CONTEXT *hd, void *blockof64byte)
{
  uint32_t *p = blockof64byte;
  unsigned int nburn;

  nburn = transform (hd, blockof64byte, 1);
  p[0] = hd->h0;
  p[1] = hd->h1;
  p[2] = hd->h2;
  p[3] = hd->h3;
  p[4] = hd->h4;

  return nburn;
}

int main(int argc, char* argv[]) {
	if (argc != 7) {
		printf("Missing arguments\n");
		return 1;
	}
	int h0 = (int)strtol(argv[1], NULL, 16);
	int h1 = (int)strtol(argv[2], NULL, 16);
	int h2 = (int)strtol(argv[3], NULL, 16);
	int h3 = (int)strtol(argv[4], NULL, 16);
	int h4 = (int)strtol(argv[5], NULL, 16);

	unsigned char buf[65];
	char str[3];
	for (int i = 0; i < 128; i+=2) {
		str[0] = argv[6][i];
		str[1] = argv[6][i+1];
		str[2] = 0;
		buf[i/2] = (char)strtol(str, NULL, 16);
	}
	buf[64] = 0;

	SHA1_CONTEXT sha1;
	sha1.h0 = h0;
	sha1.h1 = h1;
	sha1.h2 = h2;
	sha1.h3 = h3;
	sha1.h4 = h4;

	transform(&sha1, buf, 1);
	uint32_t arr[5];

	printf("%08x%08x%08x%08x%08x\n", sha1.h0, sha1.h1, sha1.h2, sha1.h3, sha1.h4);
	arr[0] = sha1.h0;
	arr[1] = sha1.h1;
	arr[2] = sha1.h2;
	arr[3] = sha1.h3;
	arr[4] = sha1.h4;

	return 0;
}

