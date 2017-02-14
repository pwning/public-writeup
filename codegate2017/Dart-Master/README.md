## Dart Master - Pwnable

There is a trivial information leak bug and a Use-After-Free bug in the program.


#### Memory leak

Since there is no check on `i` when viewing other players' information, we can leak memory near `players`.

```
...
  if ( (signed int)i > 1 )
  {
    std::operator<<<std::char_traits<char>>(&std::cout, "Which one do you wanna see? ");
    std::istream::operator>>(&std::cin, &i);
    if ( players[i] )
    {
        ...
    }
    ...
  }
...
```


#### UAF
In `main`, the game state is deleted when the player logs out. The pointer does not get set to NULL. However, this pointer is used for generating a new ID, which results in an exploitable use-after-free condition. Also, by having the second/third players registered and deleted, we can force memory to coalesce so we can easily exploit.
