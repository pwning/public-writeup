#include <NTL/mat_GF2.h>
#include <NTL/vec_GF2.h>
#include <NTL/ZZ.h>
#include <bits/stdc++.h>
#include <cstdio>
#include <cstdint>

#define int long long
#define uint uint64_t
#define N (64 * 64)

NTL::vec_GF2 state;
NTL::mat_GF2 adv;

void advance(const NTL::ZZ& amt) {
	state = state * NTL::power(adv, amt);
}

NTL::ZZ getrand() {
	NTL::ZZ s0, s1;
	for (int i = 0; i < 64; i++) {
		if (NTL::IsOne(state[i+ 0])) NTL::SetBit(s0, i);
		if (NTL::IsOne(state[i+64])) NTL::SetBit(s1, i);
	}
	//std::cout << s0 << " " << s1 << std::endl;
	return NTL::trunc_ZZ(s0 + s1, 64);
}

main(int argc, char** argv) {
	adv.SetDims(N, N);
	FILE* matf = fopen("./matrix.txt", "r");
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			int c = fgetc(matf);
			adv.put(i, j, c == '1' ? 1 : 0);
		}
	}
	assert(fgetc(matf) == EOF);
	fclose(matf);


	state.SetLength(N);
	for (int i = 0; i < 64; i++) {
		for (int j = 0; j < 64; j++) {
			//std::cout << i << " " << j << " " << (i & (1 << j)) << std::endl;

			if (j < 30 && i & (1 << j)) {
				state.put(i*64 + j, 1);
			}
		}
	}

	//std::cout << state << std::endl;
	//std::cout << getrand() << std::endl;
	FILE* enced = fopen("./enc.dat", "rb");
	NTL::ZZ firststep(31337);
	advance(firststep);
	//std::cout << state << std::endl;
	//std::cout << getrand() << std::endl;
	std::string result;

	int cur, x = 0;
	while ((cur = fgetc(enced)) != EOF) {
		firststep = 1;
		NTL::ZZ buf = getrand();
		advance(firststep);
		int sh = x / 2;
		if (sh > 64) sh = 64;
		NTL::trunc(buf, buf, sh);
		advance(buf);
		result.push_back((unsigned char)(cur ^ NTL::trunc_long(getrand(), 8)));
		advance(firststep);
		std::cout << result << std::endl;
		x++;
	}
	fclose(enced);

	/*
	NTL::vec_GF2 vec;
	vec.SetLength(N);
	for (int i = 0; i < N; i++) vec.put(i, getchar() - '0');
	assert(getchar() == EOF);

	uint pow = strtoull(argv[1], nullptr, 10);

	NTL::mat_GF2 powed = NTL::power(adv, pow);
	vec = vec * powed;
	for (int i = 0; i < N; i++) std::cout << vec[i] ? '1' : '0';
	*/

}
