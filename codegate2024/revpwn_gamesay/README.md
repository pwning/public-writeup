# game$ay - RevPwn, 250 points (31 solves)

_Writeup by [@babaisflag](https://github.com/babaisflag)_

Description:

> Unleash your imagination within your little game console.
>
> nc 43.201.14.210 20001
>
> for\_user.zip

We're given an interpreter and a user facing game console with 5 machines, written in python.

## Reversing

The game console consists of 5 machines, each running in its own thread. Machine 0 is the privileged machine, and has preset code that it runs. For machines 1~4, initally there is no code for them to run. You have options to run all the machines that have code, run one machine, add code, or delete code (you cannot delete code in machine 0). Each machine also has a queue associated with them, which are read/writeable by itself and other machines (machine 0's queue is, however, not accessible by other machines).

Code is run by the interpreter, which is for a custom language that has a C-like syntax but with python-like functionality - notably, various built-in functions from python are, well, built in. Things that are custom to this language, however, are three builtins: `pread`, `pwrite`, and `flag`. `pread` takes the machine ID as argument and returns the item off of the queue of that machine. `pwrite` takes the machine ID and the content to write as arguments, putting the content into the machine's queue. Both of them have checks to prevent a machine with non-zero machine ID from accessing the queue of machine 0. `flag` reads the flag and returns the bytes of the flag only if the caller machine ID is 0.

The parsed code for machine 0 is in the `codes` array in `main.py`. Initially, I thought it was a python-like language so I put `__repr__` in `model.py` to print the code in a human-readable pseudo-python code. The full version is in [`p0.py`](p0.py), but the relevant part is the `main` function:

```python
def main() -> int:
    while 1:
        func_list: list = [Draw_result, Player_result, Dealer_result]
        beh: list = []
        beh_func: pointer = None
        pwrite(0, func_list)
        deck: list = initializeDeck()
        hands: list = dealCards(deck)
        playerHand: list = hands[0]
        dealerHand: list = hands[1]
        print('[Dealer]\n')
        ShowCard(dealerHand)
        print('\n[Player]\n')
        ShowCard(playerHand)
        print('\n')
        cardsToReplace: list = get_user_input()
        replaceCards(playerHand, deck, cardsToReplace)
        print('\n[Dealer]\n')
        ShowCard(dealerHand)
        print('\n[Player - Card changed]\n')
        ShowCard(playerHand)
        winner: int = determineWinner(playerHand, dealerHand)
        beh = pread(0)
        beh_func = beh[winner]
        beh_func()
        sleep(3.0)
        pwrite(0, func_list)
```

The code is a blackjack-like game. Notable things in `main` are:
- `func_list` have 3 functions for each case of the result of the game, all of which just print the result.
- `pwrite(0, func_list)` is called once here (and another time at the end of the loop, though I'm not sure why the second one is even called). It writes `func_list` to the queue of machine 0.
- After the game, the result is saved as an int from 0~2, each corresponding to draw, player win, or dealer win. These are the indices corresponding to the respective functions in `func_list`.
- Then `pread` is called, where the result is saved to `beh`; the queue contains the `func_list` from the `pwrite` above. The appropriate function is called, indexed by the saved result.

## Exploitation

There's a bug in `pread` and `pwrite`, where the permission check is done by `node.arguments[0].value == str(0) and machine_id != 0`. This checks whether `value` field of the first argument (target machine ID) as a `Node` in the AST is `"0"`. Since the interpreted result of the first argument is later used as an index to find the matching queue, it has to end up being interpreted as `0` but not have the `value` field be `"0"`. Most primitive types can't have this property and expressions with operators don't even have the `value` field, but `Group` node does, so we can bypass the check by setting the argument as `(0+0)`.

We want the object added to machine 0's queue to be an array of 3 functions which print out flag, so the exploit is the following ([`sol.c`](sol.c)):

```c
func flage() int {
    print(flag());
}

func main() int {
    while true {
        pwrite((0+0), [flage, flage, flage]);
    }
    return 0;
}
main();
```

Connect to the server, add the program in base64, run `all`, and play the black jack game twice to get the flag: `codegate2024{e6d327587465a442e34ecea8c817bb7701b55b0a73dbea7a87faa11ee25b2835dc5b430093f3c78cf14902deb9c86b9f29515d}`
