# Buggy .Net

Author: [@zwad3](https://twitter.com/zwad3)

So apparently `.net` is buggy. And Orange found the bug. And he's making us find the bug. Yay.

## Overview

Buggy `.net` is an extremely straightforward application. It's running the `.net` framework with only a tiny bit of server-side code:

```c#
bool isBad = false;
try {
    if ( Request.Form["filename"] != null ) {
        isBad = Request.Form["filename"].Contains("..") == true;
    }
} catch (Exception ex) {

}

try {
    if (!isBad) {
        Response.Write(System.IO.File.ReadAllText(@"C:\inetpub\wwwroot\" + Request.Form["filename"]));
    }
} catch (Exception ex) {

}
```

So basically, if you can cause an exception to be thrown during the first request, you have free reign to use `..` in the `filename` parameter. The question then becomes, how do we cause a crash only in the first case but not the second.

## But First, the Code

Well, when Orange says "jump", we say "how hi," so the first thing I did was crack open the `asp.net` source code. I wanted to figure out how it was parsing form data, but the `asp.net` codebase is so big, it took me a surprisingly long time to even find that. After some digging, I found [FormFeature.cs](https://github.com/aspnet/AspNetCore/blob/master/src/Http/Http/src/Features/FormFeature.cs), which has a lot of the parsing logic, as well as some adjacent modules that handle it to. I read through them for a bit before it dawned on me. Nowhere in any of this code did I see it check that the request was a `POST`. In my insomnia window, I changed the `POST` to a `GET` &mdash; still with the body &mdash; and sent it.

...

Yeah, that worked just fine.

However, that's not really useful in any way. With `filename` still set to `../../../../FLAG`, the filter was catching it and we didn't get our file read. It's non-compliant with the HTTP spec, but it's also not obviously a bug. Furthermore, I don't have anything to do with it.

## Happy Little Accident

Several time zones away, b2xiao was also looking at the `asp.net` codebase. What he saw, that I had missed, was that `asp.net` has a primitive injection filter. For instance, if you send a form that has `<!` in the value, it will automatically throw an error when parsing the request. When he told this to me, my response was "huh" let me try it out.

Just for fun, I added a new field to my request called xss set to `<!`. When I hit submit, I was more than a little surprised to see it come back with... the flag.

## Post-Mortem

So why did that work? Well, you don't look a gift horse in the mouth, especially in the middle of a CTF. My best guess, having read through a lot of `.net` code is that when you make a `POST` request, the HTTP module automatically parses the body. When it gets to the xss payload, it hits the filter and throws immediately. However, when you make a `GET` request, it doesn't think to parse the body. However, when you request the `Form` field of `Request` object, it triggers the parsing codepath. It finds the bad field, and throws an error which is now cuaght inside of the try-catch. But, parsing is expensive and you don't want to do it multiple times, so `asp.net` memoizes the form results. When we go to request it the second time, it already has the parsed results and does not throw. This allows us to read the `filename` parameter safely, without throwing an error.

This was a cute little problem, but I didn't end up spending that much time on it because through luck and some good observations, we ended up solving it after only and hour or two. Still, it was pretty fun.