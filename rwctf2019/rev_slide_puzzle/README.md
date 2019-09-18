## Slide Puzzle - rev problem - 126 points (38 solves)

### Description

Slide Puzzle is a slide puzzle app written in Flutter + Dart based off of [this sample slide puzzle app](https://flutter.github.io/samples/slide_puzzle/#/) with [source here](https://github.com/kevmoo/slide_puzzle/).

### Reversing

By playing and winning the game, we were able to observe several API calls.

| API Call | Description                                          | Request                                                             | Response                                                                                                    |
|----------|------------------------------------------------------|---------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| new_game | Used to start a new game                             |                                                                     | Base 64-encoded data with bytes as values 0x00-0x0f, each value n representing tile n+1 (or empty for 0x0f) |
| verify   | Used to verify that the player actually won the game | The series of tiles clicked for verification that the game was won. | Some chunk of base 64-encoded binary data?                                                                  |
| submit   | Submit the player's name after winning               | Player name                                                         |                                                                                                             |
| rank     | Display the scoreboard/rankings                      |                                                                     | Player rankings                                                                                             |

The `verify` API call was particularly interesting since it would return a chunk of unknown base 64-encoded data.

```json
{
    data: "I4tK9CHc8FaXWVO1+lgruQhGIXelO5yiSHaMJczA30KHW2+TSxh/lCTdHfn04rqrp9QAClf/d/cifG5wwYnCUStYT05L9zaHSw2KbbS3VszpGxYLRYWe81Z6rv8Qyg/vBF9WJ0b4Zlka6Tuajc3m0cWwVRT9XO6D14jg9E/Ngohi677kOV9Xjwq/z+OfTI6FnhRuZMPS2HbzoLccj1d4KhDZ/v2dhtQi+aTG47ylxrO7Kq1g60CZ8ib/q1I6el2vU2ITop/Oc20Bnxq/qz2951nCPVt06nfZAEB8w6s4m4qvR3iwBeXzYqOXiLo0EQoalafbxNvxscYKW+3VDAlWiu3auDEOuA3igUfGAdmJdccpcSaKAhD/pDStwK/arDZpFHr3x9LnUhfmdNgyTJm/6Ulz3D9G2ETcwnACP5xszFUnKraA8/xAytKvPiOBxKl66cPcYtGJYcuiMomP1RtactGoteN4XtWDq8XYnWojY8+EJqRSA1lmYELLbWap7EKAFgmVGjAplzNJPT/4QrAVclBVSclqIPKjT8LIAaPV6QRyWNrfsvFet6QwgeFLAvJKORmOLI2FziZ5ENhJWfeRI+QyQSI5K9H25s/U12UBtdj3CXuuW2wWFMBWBYDWBIvzSADrgcl1/RP8ylffpNpFh4VEloayxy9oPqAkjSoeeLC19TGQY4hpuf1RwLEHkArhSirpN7PhYKORqozNO/iU/nk1xqFRQK339YZ0HrEgVZp5X9IDMPxRdhDAexVi1a1awC1s0x11VVtIT2qxr4g7e4BdQniPLRdMG2UgFZiNYS16djLmOyLeMr57MJLjWZHSriHMkOVceHU+W9uX+4bt1HZ2ltlps7upv2Gel7qFeX9KrqpgNOwGr1hqmffODrI9YAbY7A+2VDQJvsNZ/sEo4oFm9mHOv3fSR8AH2yIrGmTVqASc++rUlYsgJQQDPQJPjrOnitJKqqUdZlRYfbMva0IvDgOFQabC+lDdj57SKIqMpUF+FliC8WFQHk64W8FX+pdeQK+cmaEyeFzs2/9Z9ASRFl8ExRNoVGXBTG6fZudVBrExR+IEj/LEmgdHpQXt21TWWrQ8rt7xG8REsxLzg5BFaXKs6NOoCY31RVSewNyXZvvwhf9erPi+7Ok4uzfL1heI5plxY8e6X/UrYFVFaHJwKcOJLV8qjFLuIrqDlEDeBSrx87f8QI8FOtojIPu7NLn9ARU5E69uA7ivF/KNefkHuApR9b9lK73oeBY4LiQjKFRHleO/QeOSmLBd7kK5VevjSAU4FRiwJrhHg6xo8QErwqhlY0YQSpMPHQg2mXbWJUOUhDujPHs3VMXW8JBKWLTFFSLDZvFvpUF6ejeLJkj0Qi7UFEqEWTnBjPr5p+vlBLVqCPGfS2QoNbRq0/Xvb35nz32OcAGty1D7557CKsYuE4rH72/JNS+J7h0Qosu3RC2Kwh3To/H6E8rqbi4yjfcrtThhhiJ7ebhtgRgUUm6fS+9iX8RRne6zelwcSANUg8LC6THssvukEQlZQ+10jL3xXXfMRwxm0IOpUE2ZsV6V+UG/emDGLs78cpJ66HoF3K8rWYH4wv4FlrwieM/FF4jfjfyu9krfAVJprZXkJqdo1isT8hvxcKHxpoWr8aSasPGjvqjxv5u58bi5ivGppazxq4G68Z2oqvGsorvxr6ep8aqpuvGlh5fxprGr8bOQhvGsp4LxsaSC8ZqIo/GduKrxtp6S8ayonvGYvYbxoZiz8aKtjvGugoLygqmh8aGfnvGVjr7xrImb8ZqAhPGjlLPxs6O08aecpvGtl6nxsZmO8bKYuQ==",   
    err: null,
    msg: "Congratulations!",
    success: true
}
```

We figured that we needed to reverse the Dart JS code which received this blob. We started by beautifying the 1.5 MB JS file and looking for the code that accessed `/api/verify`. This turned out to be the `A.UD` function. It's called by `E.OQ`, which calls `E.JZ` with `A.UD`'s result using a Promise-like callback mechanism. `E.JZ` evidently implements the username prompt (which is eventually sent to `/api/submit`), calling the function `E.JY` with the username.

`E.JY` is a fairly long function which is clearly doing more than just receiving the username. In order to make sense of the function, we used the Flutter SDK to compile the sample slide puzzle app to an unminified JS file for comparison purposes.

`E.JY` starts by base64-decoding the data blob, as expected. It takes the first byte of the result as a "size" value (s), then arranges the next `s * s` bytes into a 2D matrix `r` (an array of `s`-element arrays). It takes the final portion of data after the matrix and decodes that part using UTF-8 into an array of codepoints `l`. Finally, it walks over the rows of the matrix, multiplying each row with the input username and checking the sum (the dot-product) against the corresponding entry in `l`, and outputs a congratulations message if all entries match. Basically, it's checking the matrix equation `rx = l`. We can invert this very easily in Sage (see [`solve.sage`](solve.sage)), which outputs a "username" that is the flag.