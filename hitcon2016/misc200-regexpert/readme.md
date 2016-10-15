## RegExpert - Misc 200 Problem

### Description

We're asked to connect to a remote service which challenges us to solve a series of challenges with regex.

### Solution

First, by entering a malformed regex, we get an error message that indicates they are using Ruby syntax. This is quite important since some of the regex challenges involve non-regular languages: that is, they require engine-specific regular expression extensions in order to solve.

#### 1

> ================= [SQL] =================
> Please match string that contains "select" as a case insensitive subsequence.
> 
> 21 byte limit.

The limit means that you have to force the regex to be case insensitive instead of using the usual `[sS]` trick. This is easily done with the `(?i)` match modifier in Ruby.

    (?i)s.*e.*l.*e.*c.*t

#### 2

> =============== [a^nb^n] ================
> Yes, we know it is a classical example of context free grammer.
> 
> 12 byte limit.

Now we see a regex requiring matching of *balanced* `a`s and `b`s. This is really easy to do with a *recursive* regex (also called a *subexpression call* in Ruby): just match balanced a/b pairs recursively.

    ^(a\g<1>?b)$

#### 3

> ================= [x^p] =================
> A prime is a natural number greater than 1 that has no positive divisors other than 1 and itself.
> 
> 18 byte limit.

This is a classic problem. The solution is easy: use `(?!)` to fail any string that can be factored (using `(xx+)` to guess a factor and `\1+` to repeat it). This leaves only the primes. The `xx+` at the end ensures we match only strings of the right format.

    ^(?!(xx+)\1+$)xx+$

#### 4

> ============= [Palindrome] ==============
> Both "QQ" and "TAT" are palindromes, but "PPAP" is not.
> 
> 22 byte limit.

Again, a straightforward application of recursive regex.

    ^((.)\g<1>?\2|.)?$

#### 5

> ============== [a^nb^nc^n] ==============
> Is CFG too easy for you? How about some context SENSITIVE grammer?
> 
> 29 byte limit.

We can solve this by simply matching `a^nb^nc+` and `a+b^nc^n` simultaneously, combining the two constraints with a positive lookahead `(?=)` (which acts kind of like an AND operator when used this way).

    ^(?=(a\g<1>?b)c)a+(b\g<2>?c)$

### Flag

`hitcon{The pumping lemma is a lie, just like the cake}`
