Reversing, no strings attached. 
--------------------------------

We notice an “authenticate” function, which does a decryption into a buffer and compares it with the user input. We run the binary in GDB and breakpoint at the return of decrypt. 

```
autheticate () {
  // …
  s2 = (wchar_t *)decrypt(&s, &dword_8048A70);
  result = (int)fgetws(ws, 0x2000, stdin);
  if ( result )
  {
    ws[wcslen(ws) - 1] = 0;
    if ( !wcscmp(ws, s2) )
      result = wprintf(&unk_8048B24);
    else
      result = wprintf(&unk_8048B84);
  }
  // …
}
```

We note that it is not a regular string but a wide string from the wcscmp function. Therefore, displaying the memory address around the decrypted pointer, we get:

```
(gdb) x/40c $eax
0x804b948:  57 '9'  0 '\000'    0 '\000'    0 '\000'    52 '4'  0 '\000'    0 '\000'  0 '\000'
0x804b950:  52 '4'  0 '\000'    0 '\000'    0 '\000'    55 '7'  0 '\000'    0 '\000'  0 '\000'
0x804b958:  123 '{' 0 '\000'    0 '\000'    0 '\000'    121 'y' 0 '\000'    0 '\000'  0 '\000'
0x804b960:  111 'o' 0 '\000'    0 '\000'    0 '\000'    117 'u' 0 '\000'    0 '\000'  0 '\000'
0x804b968:  95 '_'  0 '\000'    0 '\000'    0 '\000'    97 'a'  0 '\000'    0 '\000'  0 '\000'
```

We notice dumping the memory gives us the entire flag where each character of the flag is separated by 12 bytes of null bytes. We read off the string and get:

9447{you_are_an_international_mystery}
