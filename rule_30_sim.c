
#include <stdlib.h>
#include <stdio.h>


int main() {
    __uint128_t curr = *(__uint128_t *)"DiceGangDanceGig";
    __uint128_t left, right;

    for (uint64_t i = 0; i < 1000000000000; ++i) {
        if (i % 1000000000 == 0 || (i < 100)) {
            printf("%llu: ", i);
            printf("0x%016llx%016llx\n", (uint64_t)(curr >> 64), (uint64_t)curr);
        }

        right = (curr >> 1) | ((curr & 1) << 127);
        left = (curr << 1) | (curr >> 127);

        curr = left ^ (curr | right);
    }

    printf("0x%016llx%016llx\n", (uint64_t)(curr >> 64), (uint64_t)curr);
}


// 0: 0x67694765636e6144676e614765636944
// 1000000000: 0x1525ccbe6e54a4882121ec282036a852
// 2000000000: 0x2b8fa044a0e7b2870a6f49ecf528164f
// 3000000000: 0xc7ed77443d79ce3136c1547a525279bb
// 4000000000: 0x37166f666b1a397a92ece5a0b35ed164
// 5000000000: 0xbd9511810b18c2413f5e5b3be258b484

// 0: 0x67694765636e6144676e614765636944
// 1000000000: 0x1525ccbe6e54a4882121ec282036a852
// 2000000000: 0x2b8fa044a0e7b287a6f49ecf528164f
// 3000000000: 0xc7ed77443d79ce3136c1547a525279bb