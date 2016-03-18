## JS_is_not_a_jail - Misc 100 Problem

We are given access to a v8 interpreter, which upon connection tells us to run
the challenge100() function. By just sending challenge100, we get the function
code:

```javascript
function (arr) {
        var random_value = "ac1a39300ce7ee8b6cff8021fd7b0b5caf5bc1c316697bd8f22e00f9fab710d6b8dba23ca80f6d80ca697e7aa26fd5f6";
        var check = "20150303";

        if((arr === null || arr === undefined)) {
            print("arr is null or undefined.");
            return;
        }

        if(!arr.hasOwnProperty('length')) {
            print("length property is null or undefined.");
            return;
        }

        if(arr.length >= 0) {
            print("i think you're not geek. From now on, a GEEK Only!");
            return;
        }

        if(Object.getPrototypeOf(arr) !== Array.prototype) {
            print("Oh.... can you give me an array?");
            return;
        }

        var length = check.length;
        for(var i=0;i<length;i++) {
            arr[i] = random_value[Math.floor(Math.random() * random_value.length)];
        }

        for(i=0;i<length;i++) {
            if(arr[i] !== check[i]) {
                print("Umm... i think 2015/03/03 is so special day.\nso you must set random value to 20150303 :)");
                return;
            }
        }
        print("Yay!!");
        print(flag);
    }
```

This function checks that the argument given is a Array-like object whose
length is less than 0 and contains the characters from the string *20150303*.
The basic process for doing this is to create a new Object that has the
Array prototype, and then define some getters for *length*, *0*, *1*, etc.

```
d8> C = Object.create(Array.prototype)
d8> C.__defineGetter__('length', function() { return -1; })
d8> C.__defineGetter__('0', function() { return '2'; })
d8> C.__defineGetter__('1', function() { return '0'; })
d8> C.__defineGetter__('2', function() { return '1'; })
d8> C.__defineGetter__('3', function() { return '5'; })
d8> C.__defineGetter__('4', function() { return '0'; })
d8> C.__defineGetter__('5', function() { return '3'; })
d8> C.__defineGetter__('6', function() { return '0'; })
d8> C.__defineGetter__('7', function() { return '3'; })
d8> C.length
-1
d8> C[0]
"2"
d8> challenge100(C)
Yay!!
flag is "easy xD, get a more hardest challenge!"
```
