## Butterfree

We are given a source code file (ArrayPrototype.cpp) from WebKit project.

When we diff'd with the branch from November, 2018, we noted that length check was commented out.

```diff
--- ArrayPrototype.cpp.orig    2019-01-26 05:19:26.000000000 -0600
+++ ArrayPrototype.cpp    2019-01-15 03:35:52.000000000 -0600
@@ -973,7 +973,7 @@
     if (UNLIKELY(speciesResult.first == SpeciesConstructResult::Exception))
         return { };

-    bool okToDoFastPath = speciesResult.first == SpeciesConstructResult::FastPath && isJSArray(thisObj) && length == toLength(exec, thisObj);
+    bool okToDoFastPath = speciesResult.first == SpeciesConstructResult::FastPath && isJSArray(thisObj) /*&& length == toLength(exec, thisObj)*/;
     RETURN_IF_EXCEPTION(scope, { });
     if (LIKELY(okToDoFastPath)) {
         if (JSArray* result = asArray(thisObj)->fastSlice(*exec, begin, end - begin))
```

This vulnerability is basically the same as CVE-2016-4622, which was covered in detail by saelo (http://www.phrack.org/papers/attacking_javascript_engines.html).



However, it turns out that the author did not carefully remove `jsc` built-ins such as `readFile`. So instead of pwning the Javascript memory corruption bug, we could trivially read the flag file.

```
>>> readFile('./flag')
flag{4240a8444fe8734044fca90700b3ade2}
```

