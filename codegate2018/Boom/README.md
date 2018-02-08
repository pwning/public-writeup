## Boom - Reversing Challenge

We are given a compiled Rust binary to reverse. There are 7 different puzzles and each puzzle leads to a different one. The goal is to solve at least 4 of them and trigger the check function.

There are 7 puzzle functions:

* Function #1
  * You need to send a hidden clause, and there are three possibilities
    * "Know what? It's a new day~" leads to Function #2
    * "It's cold outside.." leads to Function #3
    * "We need little break!" leads to Function #5
* Function #2
  * Substitution cipher, where you need to send one of three sets of numbers
    * carame1
      * 3 14 7 14 60 1 26
      * leads to Function #4
    * w33kend
      * 64 15 15 31 1 23 13
      * leads to Function #5
    * pand0ra
      * 57 14 23 13 50 7 14
      * leads to Function #7
* Function #3
  * You need to solve a cube in 6 or less steps
    * B B R R L T
    * leads to Function #6
* Function #4
  * We didn't know what it actually was doing, but it takes 4 digits
  * Seemed like any permutation of 1, 5, 3, 8 worked
    * 1 5 3 8
    * leads to Function #6
* Function #5
  * You need to provide one of the hailstone numbers for 107
    * Any of 31, 188, 189, 190
    * leads to Function #4
* Function #6
  * You need to decrypt one of the two strings
    * H_vocGfsg4p_xicwcrwexg4r
      * Dark_Choc0late_sensati0n
      * leads to Function #2
    * G_veqijcGvi_qcL4rcGl4a44
      * Caramel_Cream_H0t_Ch0c00
      * leads to Function #7
* Function #7
  * You need to provide magic sqaure numbers (for 5x5)
    * 17 24 1 8 15 23 5 7 14 16 4 6 13 20 22 10 12 19 21 3 11 18 25 2 9
    * leads to Function #5



Also, we need to take the path in specific order: `func1->func2->func7->func5`

```
Know what? It's a new day~
57 14 23 13 50 7 14
17 24 1 8 15 23 5 7 14 16 4 6 13 20 22 10 12 19 21 3 11 18 25 2 9
190
1 1 1 1
```

Note that last line triggers a wrong answer for Function #4, which will trigger the check function and eventually the win function that reads the flag to us.