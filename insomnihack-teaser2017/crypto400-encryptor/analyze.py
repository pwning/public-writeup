code = '''
vmovdqa ymm0, ymmword ptr [constants]
vmovdqa ymm5, ymmword ptr [keys]
vmovdqa ymm2, ymmword ptr [inblock]
vmovdqa ymm8, ymmword ptr [inblock+60h]
vpmulhuw ymm1, ymm2, ymm5
vpmullw ymm6, ymm2, ymm5
vpsubusw ymm3, ymm6, ymm1
vpcmpeqw ymm3, ymm0, ymm3
vpsubw  ymm6, ymm6, ymm1
vmovdqa ymm4, ymmword ptr [keys+60h]
vpor    ymm2, ymm2, ymm5
vmovdqa ymm11, ymmword ptr [inblock+40h]
vpmulhuw ymm7, ymm8, ymm4
vpmullw ymm9, ymm8, ymm4
vpor    ymm4, ymm8, ymm4
vpsrlw  ymm3, ymm3, 0Fh
vpaddw  ymm3, ymm3, ymm6
vpcmpeqw ymm6, ymm6, ymm0
vpsubusw ymm1, ymm9, ymm7
vpsubw  ymm9, ymm9, ymm7
vpaddw  ymm11, ymm11, ymmword ptr [keys+40h]
vpcmpeqw ymm1, ymm1, ymm0
vmovdqa ymm13, ymmword ptr [keys+0C0h]
vpand   ymm5, ymm2, ymm6
vmovdqa ymm2, ymmword ptr [inblock+20h]
vpsrlw  ymm1, ymm1, 0Fh
vpaddw  ymm1, ymm1, ymm9
vpaddw  ymm2, ymm2, ymmword ptr [keys+20h]
vpsubw  ymm5, ymm3, ymm5
vpcmpeqw ymm3, ymm9, ymm0
vpxor   ymm7, ymm11, ymm5
vpand   ymm4, ymm4, ymm3
vmovdqa ymm3, ymmword ptr [keys+80h]
vpmullw ymm6, ymm7, ymm3
vpsubw  ymm10, ymm1, ymm4
vpmulhuw ymm1, ymm7, ymm3
vpor    ymm3, ymm3, ymm7
vpsubusw ymm4, ymm6, ymm1
vpsubw  ymm6, ymm6, ymm1
vpcmpeqw ymm1, ymm6, ymm0
vpxor   ymm8, ymm10, ymm2
vmovdqa ymm7, ymmword ptr [constants+40h]
vpcmpeqw ymm4, ymm4, ymm0
vpand   ymm3, ymm3, ymm1
vpsrlw  ymm4, ymm4, 0Fh
vpaddw  ymm4, ymm4, ymm6
vpsubw  ymm1, ymm4, ymm3
vpaddw  ymm8, ymm1, ymm8
vpshufhw ymm6, ymm8, 93h
vmovdqa ymm4, ymmword ptr [constants+20h]
vpshuflw ymm6, ymm6, 93h
vpxor   ymm8, ymm6, ymm8
vpsllw  ymm9, ymm8, 1
vpshufhw ymm3, ymm8, 4Eh
vpand   ymm8, ymm4, ymm8
vpxor   ymm6, ymm6, ymm9
vmovdqa ymm9, ymmword ptr [keys+0A0h]
vpshuflw ymm3, ymm3, 4Eh
vpcmpeqw ymm8, ymm8, ymm4
vpxor   ymm3, ymm6, ymm3
vpand   ymm8, ymm7, ymm8
vpxor   ymm3, ymm8, ymm3
vpmullw ymm8, ymm3, ymm9
vpmulhuw ymm12, ymm3, ymm9
vpsubusw ymm6, ymm8, ymm12
vpcmpeqw ymm6, ymm6, ymm0
vpsubw  ymm12, ymm8, ymm12
vpor    ymm3, ymm9, ymm3
vmovdqa ymm9, ymmword ptr [constants+200h]
vpsrlw  ymm6, ymm6, 0Fh
vpaddw  ymm8, ymm6, ymm12
vpcmpeqw ymm6, ymm12, ymm0
vpand   ymm6, ymm3, ymm6
vmovdqa ymm3, ymmword ptr [constants+240h]
vmovdqa [rbp+var_30], ymm3
vpsubw  ymm6, ymm8, ymm6
vpxor   ymm5, ymm5, ymm6
vpaddw  ymm1, ymm6, ymm1
vpxor   ymm2, ymm2, ymm1
vmovdqa ymm8, ymmword ptr [constants+220h]
vpxor   ymm1, ymm10, ymm1
vpmullw ymm14, ymm5, ymm13
vpxor   ymm6, ymm11, ymm6
vmovdqa ymm11, ymmword ptr [keys+120h]
vpshufb ymm2, ymm2, ymm8
vpshufb ymm1, ymm1, ymm3
vpmulhuw ymm3, ymm5, ymm13
vpsubusw ymm10, ymm14, ymm3
vpcmpeqw ymm10, ymm10, ymm0
vpsubw  ymm14, ymm14, ymm3
vpor    ymm5, ymm13, ymm5
vpaddw  ymm2, ymm2, ymmword ptr [keys+100h]
vmovdqa ymm13, ymmword ptr [keys+140h]
vpshufb ymm6, ymm6, ymm9
vpmullw ymm15, ymm1, ymm11
vpmulhuw ymm12, ymm1, ymm11
vpsubusw ymm3, ymm15, ymm12
vpsrlw  ymm10, ymm10, 0Fh
vpcmpeqw ymm3, ymm3, ymm0
vpaddw  ymm10, ymm10, ymm14
vpsubw  ymm12, ymm15, ymm12
vpor    ymm1, ymm11, ymm1
vpaddw  ymm6, ymm6, ymmword ptr [keys+0E0h]
vpcmpeqw ymm14, ymm14, ymm0
vpsrlw  ymm3, ymm3, 0Fh
vpaddw  ymm3, ymm3, ymm12
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm5, ymm5, ymm14
vpand   ymm12, ymm1, ymm12
vpsubw  ymm5, ymm10, ymm5
vpxor   ymm10, ymm2, ymm5
vpsubw  ymm3, ymm3, ymm12
vpmulhuw ymm1, ymm10, ymm13
vpmullw ymm11, ymm10, ymm13
vpsubusw ymm12, ymm11, ymm1
vpcmpeqw ymm12, ymm12, ymm0
vpsubw  ymm11, ymm11, ymm1
vpor    ymm10, ymm13, ymm10
vpsrlw  ymm12, ymm12, 0Fh
vpaddw  ymm12, ymm12, ymm11
vpcmpeqw ymm11, ymm11, ymm0
vpand   ymm1, ymm10, ymm11
vpsubw  ymm1, ymm12, ymm1
vpxor   ymm12, ymm3, ymm6
vpaddw  ymm12, ymm1, ymm12
vpshufhw ymm11, ymm12, 93h
vpshuflw ymm11, ymm11, 93h
vpxor   ymm12, ymm11, ymm12
vpand   ymm10, ymm12, ymm4
vpsllw  ymm14, ymm12, 1
vpshufhw ymm13, ymm12, 4Eh
vpxor   ymm11, ymm11, ymm14
vpcmpeqw ymm10, ymm10, ymm4
vpshuflw ymm13, ymm13, 4Eh
vpand   ymm10, ymm7, ymm10
vpxor   ymm13, ymm11, ymm13
vpxor   ymm10, ymm10, ymm13
vmovdqa ymm13, ymmword ptr [keys+160h]
vpmullw ymm11, ymm10, ymm13
vpmulhuw ymm12, ymm10, ymm13
vpsubusw ymm15, ymm11, ymm12
vpcmpeqw ymm15, ymm15, ymm0
vpsubw  ymm12, ymm11, ymm12
vmovdqa ymm11, ymmword ptr [keys+180h]
vpor    ymm10, ymm13, ymm10
vmovdqa ymm13, ymmword ptr [keys+1E0h]
vpsrlw  ymm15, ymm15, 0Fh
vpaddw  ymm15, ymm15, ymm12
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm10, ymm10, ymm12
vpsubw  ymm15, ymm15, ymm10
vpxor   ymm5, ymm5, ymm15
vpaddw  ymm1, ymm15, ymm1
vpxor   ymm6, ymm6, ymm1
vpxor   ymm3, ymm3, ymm1
vpmullw ymm14, ymm5, ymm11
vpmulhuw ymm1, ymm5, ymm11
vpsubusw ymm10, ymm14, ymm1
vpcmpeqw ymm10, ymm10, ymm0
vpsubw  ymm14, ymm14, ymm1
vpshufb ymm3, ymm3, [rbp+var_30]
vpor    ymm5, ymm11, ymm5
vpsrlw  ymm10, ymm10, 0Fh
vpaddw  ymm10, ymm10, ymm14
vpcmpeqw ymm14, ymm14, ymm0
vpmulhuw ymm1, ymm3, ymm13
vpxor   ymm2, ymm2, ymm15
vpmullw ymm15, ymm3, ymm13
vpshufb ymm6, ymm6, ymm8
vpsubusw ymm12, ymm15, ymm1
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm5, ymm5, ymm14
vpsubw  ymm15, ymm15, ymm1
vpor    ymm3, ymm13, ymm3
vpaddw  ymm6, ymm6, ymmword ptr [keys+1C0h]
vpsrlw  ymm12, ymm12, 0Fh
vpaddw  ymm12, ymm12, ymm15
vpsubw  ymm10, ymm10, ymm5
vpcmpeqw ymm15, ymm15, ymm0
vmovdqa ymm1, ymmword ptr [keys+200h]
vpxor   ymm11, ymm6, ymm10
vpshufb ymm2, ymm2, ymm9
vpand   ymm15, ymm3, ymm15
vpmulhuw ymm13, ymm11, ymm1
vpmullw ymm3, ymm11, ymm1
vpsubusw ymm5, ymm3, ymm13
vpcmpeqw ymm5, ymm5, ymm0
vpsubw  ymm3, ymm3, ymm13
vpaddw  ymm2, ymm2, ymmword ptr [keys+1A0h]
vpor    ymm1, ymm1, ymm11
vpsubw  ymm12, ymm12, ymm15
vpxor   ymm15, ymm12, ymm2
vpsrlw  ymm5, ymm5, 0Fh
vpaddw  ymm5, ymm5, ymm3
vpcmpeqw ymm3, ymm3, ymm0
vpand   ymm1, ymm1, ymm3
vpsubw  ymm5, ymm5, ymm1
vpaddw  ymm15, ymm5, ymm15
vpshufhw ymm1, ymm15, 93h
vpshuflw ymm1, ymm1, 93h
vpxor   ymm15, ymm1, ymm15
vpand   ymm11, ymm15, ymm4
vpsllw  ymm13, ymm15, 1
vpshufhw ymm3, ymm15, 4Eh
vpxor   ymm1, ymm1, ymm13
vmovdqa ymm13, ymmword ptr [keys+240h]
vpcmpeqw ymm11, ymm11, ymm4
vpshuflw ymm3, ymm3, 4Eh
vpand   ymm11, ymm7, ymm11
vpxor   ymm3, ymm1, ymm3
vmovdqa ymm1, ymmword ptr [keys+220h]
vpxor   ymm11, ymm11, ymm3
vpmullw ymm3, ymm11, ymm1
vpmulhuw ymm15, ymm11, ymm1
vpsubusw ymm14, ymm3, ymm15
vpcmpeqw ymm14, ymm14, ymm0
vpsubw  ymm15, ymm3, ymm15
vpor    ymm11, ymm1, ymm11
vpsrlw  ymm14, ymm14, 0Fh
vpaddw  ymm14, ymm14, ymm15
vpcmpeqw ymm15, ymm15, ymm0
vpand   ymm1, ymm11, ymm15
vpsubw  ymm1, ymm14, ymm1
vpxor   ymm10, ymm10, ymm1
vpaddw  ymm5, ymm1, ymm5
vpxor   ymm2, ymm2, ymm5
vpxor   ymm5, ymm12, ymm5
vpmulhuw ymm3, ymm10, ymm13
vpmullw ymm14, ymm10, ymm13
vpsubusw ymm11, ymm14, ymm3
vpcmpeqw ymm11, ymm11, ymm0
vpsubw  ymm14, ymm14, ymm3
vpshufb ymm5, ymm5, [rbp+var_30]
vpxor   ymm1, ymm6, ymm1
vmovdqa ymm6, ymmword ptr [keys+2A0h]
vpor    ymm10, ymm13, ymm10
vpsrlw  ymm11, ymm11, 0Fh
vpaddw  ymm11, ymm11, ymm14
vpmullw ymm15, ymm5, ymm6
vpmulhuw ymm12, ymm5, ymm6
vpcmpeqw ymm14, ymm14, ymm0
vpsubusw ymm3, ymm15, ymm12
vpor    ymm5, ymm6, ymm5
vpsubw  ymm12, ymm15, ymm12
vpcmpeqw ymm3, ymm3, ymm0
vpshufb ymm2, ymm2, ymm8
vpand   ymm10, ymm10, ymm14
vmovdqa ymm6, ymmword ptr [keys+2C0h]
vpshufb ymm1, ymm1, ymm9
vpsrlw  ymm3, ymm3, 0Fh
vpaddw  ymm3, ymm3, ymm12
vpcmpeqw ymm12, ymm12, ymm0
vpaddw  ymm2, ymm2, ymmword ptr [keys+280h]
vpsubw  ymm11, ymm11, ymm10
vpxor   ymm10, ymm2, ymm11
vpaddw  ymm1, ymm1, ymmword ptr [keys+260h]
vpand   ymm12, ymm5, ymm12
vpmulhuw ymm5, ymm10, ymm6
vpsubw  ymm3, ymm3, ymm12
vpmullw ymm12, ymm10, ymm6
vpsubusw ymm13, ymm12, ymm5
vpcmpeqw ymm13, ymm13, ymm0
vpsubw  ymm12, ymm12, ymm5
vpor    ymm6, ymm6, ymm10
vpsrlw  ymm13, ymm13, 0Fh
vpaddw  ymm13, ymm13, ymm12
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm5, ymm6, ymm12
vpxor   ymm12, ymm3, ymm1
vpsubw  ymm5, ymm13, ymm5
vpaddw  ymm12, ymm5, ymm12
vpshufhw ymm6, ymm12, 93h
vpshuflw ymm6, ymm6, 93h
vpxor   ymm12, ymm6, ymm12
vpand   ymm10, ymm12, ymm4
vpsllw  ymm14, ymm12, 1
vpshufhw ymm13, ymm12, 4Eh
vpxor   ymm6, ymm6, ymm14
vpcmpeqw ymm10, ymm10, ymm4
vpshuflw ymm13, ymm13, 4Eh
vpand   ymm10, ymm7, ymm10
vpxor   ymm13, ymm6, ymm13
vpxor   ymm10, ymm10, ymm13
vmovdqa ymm13, ymmword ptr [keys+2E0h]
vpmullw ymm6, ymm10, ymm13
vpmulhuw ymm12, ymm10, ymm13
vpsubusw ymm15, ymm6, ymm12
vpcmpeqw ymm15, ymm15, ymm0
vpsubw  ymm12, ymm6, ymm12
vpor    ymm10, ymm13, ymm10
vmovdqa ymm13, ymmword ptr [keys+300h]
vpsrlw  ymm15, ymm15, 0Fh
vpaddw  ymm15, ymm15, ymm12
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm10, ymm10, ymm12
vpsubw  ymm15, ymm15, ymm10
vpxor   ymm11, ymm11, ymm15
vpaddw  ymm5, ymm15, ymm5
vpxor   ymm3, ymm3, ymm5
vpxor   ymm1, ymm1, ymm5
vpmullw ymm14, ymm11, ymm13
vpmulhuw ymm5, ymm11, ymm13
vpsubusw ymm10, ymm14, ymm5
vpshufb ymm3, ymm3, [rbp+var_30]
vpsubw  ymm14, ymm14, ymm5
vmovdqa ymm5, ymmword ptr [keys+360h]
vpcmpeqw ymm10, ymm10, ymm0
vpxor   ymm2, ymm2, ymm15
vpmulhuw ymm12, ymm3, ymm5
vpmullw ymm15, ymm3, ymm5
vpor    ymm11, ymm13, ymm11
vpsubusw ymm6, ymm15, ymm12
vpsrlw  ymm10, ymm10, 0Fh
vpcmpeqw ymm6, ymm6, ymm0
vpaddw  ymm10, ymm10, ymm14
vpsubw  ymm12, ymm15, ymm12
vpor    ymm3, ymm5, ymm3
vpcmpeqw ymm14, ymm14, ymm0
vpshufb ymm1, ymm1, ymm8
vpsrlw  ymm6, ymm6, 0Fh
vpaddw  ymm6, ymm6, ymm12
vmovdqa ymm5, ymmword ptr [keys+380h]
vpcmpeqw ymm12, ymm12, ymm0
vpshufb ymm2, ymm2, ymm9
vpand   ymm11, ymm11, ymm14
vpaddw  ymm1, ymm1, ymmword ptr [keys+340h]
vpand   ymm12, ymm3, ymm12
vpaddw  ymm2, ymm2, ymmword ptr [keys+320h]
vpsubw  ymm10, ymm10, ymm11
vpxor   ymm11, ymm1, ymm10
vpsubw  ymm6, ymm6, ymm12
vpmulhuw ymm3, ymm11, ymm5
vpmullw ymm12, ymm11, ymm5
vpsubusw ymm13, ymm12, ymm3
vpcmpeqw ymm13, ymm13, ymm0
vpsubw  ymm12, ymm12, ymm3
vpor    ymm5, ymm5, ymm11
vpsrlw  ymm13, ymm13, 0Fh
vpaddw  ymm13, ymm13, ymm12
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm3, ymm5, ymm12
vpxor   ymm12, ymm6, ymm2
vpsubw  ymm3, ymm13, ymm3
vpaddw  ymm12, ymm3, ymm12
vpshufhw ymm5, ymm12, 93h
vpshuflw ymm5, ymm5, 93h
vpxor   ymm12, ymm5, ymm12
vpand   ymm11, ymm12, ymm4
vpsllw  ymm14, ymm12, 1
vpshufhw ymm13, ymm12, 4Eh
vpxor   ymm5, ymm5, ymm14
vpcmpeqw ymm11, ymm11, ymm4
vpshuflw ymm13, ymm13, 4Eh
vpand   ymm11, ymm7, ymm11
vpxor   ymm13, ymm5, ymm13
vpxor   ymm11, ymm11, ymm13
vmovdqa ymm13, ymmword ptr [keys+3A0h]
vpmullw ymm5, ymm11, ymm13
vpmulhuw ymm12, ymm11, ymm13
vpsubusw ymm15, ymm5, ymm12
vpcmpeqw ymm15, ymm15, ymm0
vpsubw  ymm12, ymm5, ymm12
vpor    ymm11, ymm13, ymm11
vmovdqa ymm13, ymmword ptr [keys+3C0h]
vpsrlw  ymm15, ymm15, 0Fh
vpaddw  ymm15, ymm15, ymm12
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm11, ymm11, ymm12
vpsubw  ymm15, ymm15, ymm11
vpxor   ymm10, ymm10, ymm15
vpaddw  ymm3, ymm15, ymm3
vpxor   ymm6, ymm6, ymm3
vmovdqa ymm11, ymmword ptr [keys+420h]
vpxor   ymm2, ymm2, ymm3
vpmulhuw ymm5, ymm10, ymm13
vpmullw ymm14, ymm10, ymm13
vpsubusw ymm3, ymm14, ymm5
vpshufb ymm6, ymm6, [rbp+var_30]
vpsubw  ymm14, ymm14, ymm5
vpcmpeqw ymm3, ymm3, ymm0
vpxor   ymm1, ymm1, ymm15
vpor    ymm10, ymm13, ymm10
vpmullw ymm15, ymm6, ymm11
vpmulhuw ymm12, ymm6, ymm11
vpsubusw ymm5, ymm15, ymm12
vpsrlw  ymm3, ymm3, 0Fh
vpcmpeqw ymm5, ymm5, ymm0
vpaddw  ymm3, ymm3, ymm14
vpsubw  ymm12, ymm15, ymm12
vpor    ymm6, ymm11, ymm6
vpcmpeqw ymm14, ymm14, ymm0
vpshufb ymm2, ymm2, ymm8
vpsrlw  ymm5, ymm5, 0Fh
vpaddw  ymm5, ymm5, ymm12
vpshufb ymm1, ymm1, ymm9
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm10, ymm10, ymm14
vpaddw  ymm2, ymm2, ymmword ptr [keys+400h]
vpaddw  ymm1, ymm1, ymmword ptr [keys+3E0h]
vpand   ymm12, ymm6, ymm12
vpsubw  ymm10, ymm3, ymm10
vpxor   ymm13, ymm2, ymm10
vmovdqa ymm3, ymmword ptr [keys+440h]
vpsubw  ymm5, ymm5, ymm12
vpmullw ymm11, ymm13, ymm3
vpmulhuw ymm12, ymm13, ymm3
vpsubusw ymm6, ymm11, ymm12
vpcmpeqw ymm6, ymm6, ymm0
vpsubw  ymm11, ymm11, ymm12
vpor    ymm3, ymm3, ymm13
vpxor   ymm12, ymm5, ymm1
vpsrlw  ymm6, ymm6, 0Fh
vpaddw  ymm6, ymm6, ymm11
vpcmpeqw ymm11, ymm11, ymm0
vpand   ymm3, ymm3, ymm11
vpsubw  ymm6, ymm6, ymm3
vpaddw  ymm12, ymm6, ymm12
vpshufhw ymm11, ymm12, 93h
vpshuflw ymm11, ymm11, 93h
vpxor   ymm12, ymm11, ymm12
vpand   ymm3, ymm12, ymm4
vpsllw  ymm14, ymm12, 1
vpshufhw ymm13, ymm12, 4Eh
vpxor   ymm11, ymm11, ymm14
vpcmpeqw ymm3, ymm3, ymm4
vpshuflw ymm13, ymm13, 4Eh
vpand   ymm3, ymm7, ymm3
vpxor   ymm13, ymm11, ymm13
vpxor   ymm3, ymm3, ymm13
vmovdqa ymm13, ymmword ptr [keys+460h]
vpmullw ymm11, ymm3, ymm13
vpmulhuw ymm12, ymm3, ymm13
vpsubusw ymm15, ymm11, ymm12
vpcmpeqw ymm15, ymm15, ymm0
vpsubw  ymm12, ymm11, ymm12
vpor    ymm3, ymm13, ymm3
vmovdqa ymm13, ymmword ptr [keys+480h]
vpsrlw  ymm15, ymm15, 0Fh
vpaddw  ymm15, ymm15, ymm12
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm3, ymm3, ymm12
vmovdqa ymm12, ymmword ptr [keys+4E0h]
vpsubw  ymm15, ymm15, ymm3
vpxor   ymm10, ymm10, ymm15
vpaddw  ymm6, ymm15, ymm6
vpxor   ymm5, ymm5, ymm6
vpxor   ymm1, ymm1, ymm6
vpmulhuw ymm3, ymm10, ymm13
vpmullw ymm14, ymm10, ymm13
vpsubusw ymm6, ymm14, ymm3
vpshufb ymm5, ymm5, [rbp+var_30]
vpsubw  ymm14, ymm14, ymm3
vpcmpeqw ymm6, ymm6, ymm0
vpxor   ymm2, ymm2, ymm15
vpor    ymm10, ymm13, ymm10
vpmulhuw ymm3, ymm5, ymm12
vpmullw ymm15, ymm12, ymm5
vpsubusw ymm11, ymm15, ymm3
vpsrlw  ymm6, ymm6, 0Fh
vpcmpeqw ymm11, ymm11, ymm0
vpaddw  ymm6, ymm6, ymm14
vpsubw  ymm15, ymm15, ymm3
vpor    ymm5, ymm12, ymm5
vpcmpeqw ymm14, ymm14, ymm0
vpshufb ymm1, ymm1, ymm8
vpsrlw  ymm11, ymm11, 0Fh
vpaddw  ymm11, ymm11, ymm15
vpshufb ymm2, ymm2, ymm9
vpcmpeqw ymm15, ymm15, ymm0
vpand   ymm10, ymm10, ymm14
vpaddw  ymm1, ymm1, ymmword ptr [keys+4C0h]
vpaddw  ymm2, ymm2, ymmword ptr [keys+4A0h]
vpand   ymm15, ymm5, ymm15
vmovdqa ymm5, ymmword ptr [keys+500h]
vpsubw  ymm6, ymm6, ymm10
vpxor   ymm10, ymm6, ymm1
vpsubw  ymm11, ymm11, ymm15
vpmullw ymm3, ymm5, ymm10
vpmulhuw ymm12, ymm10, ymm5
vpor    ymm5, ymm5, ymm10
vpsubusw ymm15, ymm3, ymm12
vpsubw  ymm12, ymm3, ymm12
vpcmpeqw ymm3, ymm12, ymm0
vpxor   ymm10, ymm2, ymm11
vpcmpeqw ymm15, ymm15, ymm0
vpand   ymm3, ymm5, ymm3
vpsrlw  ymm15, ymm15, 0Fh
vpaddw  ymm15, ymm15, ymm12
vpsubw  ymm15, ymm15, ymm3
vpaddw  ymm10, ymm15, ymm10
vpshufhw ymm3, ymm10, 93h
vpshuflw ymm3, ymm3, 93h
vpxor   ymm10, ymm3, ymm10
vpsllw  ymm12, ymm10, 1
vpshufhw ymm5, ymm10, 4Eh
vpand   ymm10, ymm10, ymm4
vpxor   ymm3, ymm3, ymm12
vmovdqa ymm12, ymmword ptr [keys+520h]
vpshuflw ymm5, ymm5, 4Eh
vpcmpeqw ymm10, ymm10, ymm4
vpxor   ymm5, ymm3, ymm5
vpand   ymm10, ymm7, ymm10
vpxor   ymm10, ymm10, ymm5
vpmulhuw ymm3, ymm10, ymm12
vpmullw ymm5, ymm12, ymm10
vpsubusw ymm13, ymm5, ymm3
vpcmpeqw ymm13, ymm13, ymm0
vpsubw  ymm5, ymm5, ymm3
vpor    ymm10, ymm12, ymm10
vpsrlw  ymm13, ymm13, 0Fh
vpaddw  ymm13, ymm13, ymm5
vpcmpeqw ymm5, ymm5, ymm0
vpand   ymm10, ymm10, ymm5
vpsubw  ymm10, ymm13, ymm10
vpaddw  ymm15, ymm15, ymm10
vpxor   ymm2, ymm15, ymm2
vpxor   ymm15, ymm15, ymm11
vpxor   ymm6, ymm10, ymm6
vpshufb ymm3, ymm2, ymm8
vpshufb ymm2, ymm15, [rbp+var_30]
vmovdqa ymm13, ymmword ptr [keys+540h]
vpxor   ymm1, ymm10, ymm1
vmovdqa ymm11, ymmword ptr [keys+5A0h]
vpmulhuw ymm10, ymm6, ymm13
vpmullw ymm14, ymm13, ymm6
vpsubusw ymm5, ymm14, ymm10
vpcmpeqw ymm5, ymm5, ymm0
vpmullw ymm15, ymm11, ymm2
vpmulhuw ymm12, ymm2, ymm11
vpsubw  ymm14, ymm14, ymm10
vpor    ymm6, ymm13, ymm6
vpsubusw ymm10, ymm15, ymm12
vpcmpeqw ymm10, ymm10, ymm0
vpsubw  ymm12, ymm15, ymm12
vpor    ymm2, ymm11, ymm2
vpsrlw  ymm5, ymm5, 0Fh
vpaddw  ymm5, ymm5, ymm14
vpaddw  ymm3, ymm3, ymmword ptr [keys+580h]
vpcmpeqw ymm14, ymm14, ymm0
vpsrlw  ymm10, ymm10, 0Fh
vpaddw  ymm10, ymm10, ymm12
vpshufb ymm1, ymm1, ymm9
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm6, ymm6, ymm14
vmovdqa ymm14, ymmword ptr [keys+600h]
vpaddw  ymm1, ymm1, ymmword ptr [keys+560h]
vpand   ymm12, ymm2, ymm12
vmovdqa ymm2, ymmword ptr [keys+5C0h]
vpsubw  ymm5, ymm5, ymm6
vpxor   ymm6, ymm5, ymm3
vpsubw  ymm10, ymm10, ymm12
vpmulhuw ymm13, ymm6, ymm2
vpmullw ymm11, ymm2, ymm6
vpor    ymm6, ymm2, ymm6
vpsubusw ymm12, ymm11, ymm13
vpsubw  ymm11, ymm11, ymm13
vpcmpeqw ymm2, ymm11, ymm0
vpxor   ymm13, ymm1, ymm10
vpcmpeqw ymm12, ymm12, ymm0
vpand   ymm2, ymm6, ymm2
vpsrlw  ymm12, ymm12, 0Fh
vpaddw  ymm12, ymm12, ymm11
vpsubw  ymm12, ymm12, ymm2
vpaddw  ymm13, ymm12, ymm13
vpshufhw ymm2, ymm13, 93h
vpshuflw ymm2, ymm2, 93h
vpxor   ymm13, ymm2, ymm13
vpsllw  ymm11, ymm13, 1
vpshufhw ymm6, ymm13, 4Eh
vpand   ymm13, ymm13, ymm4
vpshuflw ymm6, ymm6, 4Eh
vpcmpeqw ymm4, ymm13, ymm4
vpand   ymm4, ymm7, ymm4
vpxor   ymm7, ymm2, ymm11
vpxor   ymm7, ymm7, ymm6
vpxor   ymm7, ymm4, ymm7
vmovdqa ymm4, ymmword ptr [keys+5E0h]
vpmulhuw ymm11, ymm7, ymm4
vpmullw ymm2, ymm4, ymm7
vpor    ymm7, ymm4, ymm7
vpsubusw ymm6, ymm2, ymm11
vpsubw  ymm2, ymm2, ymm11
vpcmpeqw ymm4, ymm2, ymm0
vpcmpeqw ymm6, ymm6, ymm0
vpand   ymm4, ymm7, ymm4
vpsrlw  ymm6, ymm6, 0Fh
vpaddw  ymm6, ymm6, ymm2
vpsubw  ymm4, ymm6, ymm4
vpaddw  ymm12, ymm12, ymm4
vpxor   ymm1, ymm12, ymm1
vpxor   ymm12, ymm12, ymm10
vmovdqa ymm10, ymmword ptr [keys+660h]
vpxor   ymm5, ymm4, ymm5
vpxor   ymm3, ymm4, ymm3
vpshufb ymm12, ymm12, [rbp+var_30]
vpmullw ymm4, ymm14, ymm5
vpshufb ymm8, ymm1, ymm8
vpmulhuw ymm1, ymm5, ymm14
vpshufb ymm9, ymm3, ymm9
vpsubusw ymm2, ymm4, ymm1
vpsubw  ymm4, ymm4, ymm1
vpmullw ymm6, ymm10, ymm12
vpmulhuw ymm3, ymm12, ymm10
vpor    ymm14, ymm14, ymm5
vpsubusw ymm1, ymm6, ymm3
vpcmpeqw ymm5, ymm4, ymm0
vpsubw  ymm3, ymm6, ymm3
vpor    ymm10, ymm10, ymm12
vpaddw  ymm9, ymm9, ymmword ptr [keys+620h]
vpaddw  ymm8, ymm8, ymmword ptr [keys+640h]
vpcmpeqw ymm2, ymm2, ymm0
vmovdqa ymmword ptr [outblock+20h], ymm9
vpand   ymm5, ymm14, ymm5
vmovdqa ymmword ptr [outblock+40h], ymm8
vpcmpeqw ymm1, ymm1, ymm0
vpsrlw  ymm2, ymm2, 0Fh
vpaddw  ymm2, ymm2, ymm4
vpcmpeqw ymm0, ymm3, ymm0
vpsubw  ymm5, ymm2, ymm5
vmovdqa ymmword ptr [outblock], ymm5
vpsrlw  ymm1, ymm1, 0Fh
vpaddw  ymm1, ymm1, ymm3
vpand   ymm0, ymm10, ymm0
vpsubw  ymm0, ymm1, ymm0
vmovdqa ymmword ptr [outblock+60h], ymm0
'''.strip()

print "digraph cryptBlock {"
print "ordering=in;"

fixed = [
    'ymmword ptr [constants]',
    'ymmword ptr [constants+20h]',
    'ymmword ptr [constants+40h]',
    'ymmword ptr [constants+60h]',
    'ymmword ptr [constants+200h]',
    'ymmword ptr [constants+220h]',
    'ymmword ptr [constants+240h]',
]

regs = {f:i for i,f in enumerate(fixed)}
curid = len(fixed)

for row in code.split('\n'):
    op, args = row.split(None, 1)
    args = args.split(', ')
    dst = args[0]
    srcs = args[1:]

    srcids = []
    extra = []
    for s in srcs:
        if s[0].isdigit():
            extra.append(s)
            continue
        if s not in regs:
            regs[s] = curid
            if 'inblock' in s:
                fillcolor = '#99ff99'
            else:
                fillcolor = '#999999'
            print 'a%d [label="SRC %s" style=filled fillcolor="%s"];' % (regs[s], s, fillcolor)
            curid += 1
        if regs[s] < len(fixed):
            extra.append(fixed[regs[s]])
            continue
        srcids.append(regs[s])

    if op == 'vmovdqa' and 'outblock' not in dst:
        regs[dst] = regs[srcs[0]]
        continue

    if 'outblock' in dst:
        extra.append(dst)
        fillcolor = '#ff9999'
    else:
        fillcolor = '#ffffff'

    newid = curid
    regs[dst] = newid
    print 'a%d [label="%s"  style=filled fillcolor="%s"];' % (newid, op + ' ' + ', '.join(extra), fillcolor)
    for s in srcids:
        print 'a%d -> a%d;' % (s, newid)
        #print 'a%d -> a%d;' % (newid, s)
    curid += 1

print "}"
