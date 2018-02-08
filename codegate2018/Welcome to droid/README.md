## Welcome to droid - Reversing Challenge

We are given an APK file, [droid.apk](droid.apk), which we analyze using jadx. It contains four classes:

    * MainActivity
    * Main2Activity
    * Main3Activity
    * Main4Activity

From the decompiled source code, it was obvious that none of the classes were interesting, except Main4Activity
which calls into a JNI function, *stringFromJNI*.

At this point we extracted the JNI libraries and immediately noticed that there were a large number of
included architectures: arm64, arm, armv7, mips, mips64, x86, and x86\_64. This made us consider that there
might be differences between the different architectures.

By comparing the exports, we could quickly see that the x86 library had an additional JNI function, whose name
matches with the activity that calls the JNI function.

```
lib/mips/libnative-lib.so
00004150 T Java_com_example_puing_a2018codegate_MainActivity_stringFromJNI

lib/mips64/libnative-lib.so
0000000000009490 T Java_com_example_puing_a2018codegate_MainActivity_stringFromJNI

lib/x86/libnative-lib.so
000043d0 T Java_com_example_puing_a2018codegate_Main4Activity_stringFromJNI
000042b0 T Java_com_example_puing_a2018codegate_MainActivity_stringFromJNI

lib/x86_64/libnative-lib.so
0000000000007090 T Java_com_example_puing_a2018codegate_MainActivity_stringFromJNI
```

Trying to view ```Java_com_example_puing_a2018codegate_Main4Activity_stringFromJNI``` in IDA was a mistake, because
it was very obfuscated. However, we notice that the only call into the JVM is at 0x9FC4, so we switch to dynamic
analysis.

Using a VM from www.android-x86.org and the Android NDK, we wrote a small wrapper to call the export and attached
to it using GDB:

```
int main()
{
    void *module = dlopen("./libnative-lib.so", 1);
    void (*f)(int) = dlsym(module, "Java_com_example_puing_a2018codegate_Main4Activity_stringFromJNI");
    f(0);
    return 0;
}
```

When GDB broke at 0x9FC4, we printed the contents of the ecx register and we were given the flag:

```
(gdb) x/s $ecx
0xb7b720cc: "Wol!! awesome!! FLAG{W3_w3r3_Back_70_$3v3n7een!!!} hahahah!!"
```

