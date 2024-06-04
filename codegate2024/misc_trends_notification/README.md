# trends_notification - Misc, 250 points (46 solves)

_Writeup by [@n00bi3s](https://github.com/oswalpalash)_

Description:

> I installed the Trends Notification smartphone app to be notified of the latest IT trends. After installing it, I realized that I couldn't use the trend notification button unless I was a paid user. This is a challenge that you, as a free user, must solve.
> 
> for_user.zip

We're provided with an android app `TrendsNotification.apk`.

## Decompiling the Android app

Upon decompiling the apk, with `apktool`, we notice in `AndroidManifest.xml` that the app loads on to `com.ctf.trendsnotification.MainActivity` as the only activity.
While looking for suspicious code, we notice a mention of `flag` in [src/z1/c.java](./c.java).

We identify the following pieces of relevant code:
```java
    public static final boolean encrypt_data_check(String s)
    {
        r4.h.d(s, "encrypt_data");
        return s == "0f010a0c0c121e1166656763236c68636c69676a6e6a20247524797679717675752b7b7b787b7b7c327d7fc288c2863e";
    }
```
```java
c.encrypt("flag", ((String) (obj7)));
```
```java
    public static final String encrypt(String s, String s1)
    {
    ...
    s = customOperation(xorOperation(s, s1));
```
```java
    public static final String customOperation(String s)
    {
        r4.h.d(s, "text");
        ArrayList arraylist = new ArrayList(s.length());
        int j1 = 0;
        for (int i1 = 0; j1 < s.length(); i1++)
        {
            char c1 = s.charAt(j1);
            j1++;
            arraylist.add(Character.valueOf((char)((c1 + i1) % 256)));
        }

        return j4.m.a2(arraylist, "", null, null, null, 62);
    }
```

By patching the smali file for the app, and printing out the xor key in `map.get("key")` in the activity, we see that the xor key is `lol`.
[xorkey.webp](./xorkey.webp)

Since the encrypted flag and the operations required to encrypt the flag are available statically, we write the following decryption routine.

```python
def reverse_custom_operation(encrypted_text):
    original_text = []
    c3 = 0
    for i in range(len(encrypted_text)):
        char_at = encrypted_text[i]
        original_text.append(chr((ord(char_at) - c3 + 256) % 256))  # Adjust with modulo 256 to handle wrap-around
        c3 += 1
    return ''.join(original_text)

def reverse_xor_operation(encrypted_text, key):
    length = len(encrypted_text)
    key_length = len(key)
    repeated_key = (key * (length // key_length)) + key[:length % key_length]

    original_text = []
    for i in range(length):
        original_text.append(chr(ord(encrypted_text[i]) ^ ord(repeated_key[i])))

    return ''.join(original_text)

def decrypt(encrypted_text, key):
    # Step 1: Reverse customOperation
    after_custom_operation = reverse_custom_operation(encrypted_text)

    # Step 2: Reverse xorOperation
    return reverse_xor_operation(after_custom_operation, key)
```

The solve script is implemented in [`solve.py`](./solve.py). Using this, we get our flag `codegate2024{068349869ea1d3728499f648999e8926}`
