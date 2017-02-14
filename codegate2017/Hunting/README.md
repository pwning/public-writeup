## Hunting – Binary Challenge

The Hunting binary was accessible over SSH as a setuid binary. It asked you to play a text-based fighting game, and would give you the flag if you beat the final boss. (The original version of the problem had a `system("clear")` instead of `cat`ing the flag for you; this seems like it still would have been exploitable by setting the `PATH` environment variable to a folder with a `ln -s /bin/sh ./clear` in it.)

There were several stack buffer overflows in the binary, but due to stack canaries we didn't find a way to exploit them. Presumably they were red-herrings?

Hunting only used randomness seeded with `srand(time(NULL))`, so it was possible to play the game optimally and survive indefinitely. The problem was that the final boss had 2^63-2 health, and it seems like beating him normally would have taken too long.

By exploiting a race condition, it was possible to inflict negative damage to the final boss (thus wrapping its signed-integer health negative, which would kill it). The race condition was that 'attacks' occur in temporarily-spawned threads, so using the menu system quickly would cause multiple attacks to be in-progress at the same time. The relevant attacks we used were:

* The 'fireball' attack, which does
  - Store a random 32-bit value in the (effectively) global damage_to_deal variable
  - sleep(1)
  - Interprets damage_to_deal as a 32-bit integer, and deals that much damage.

* The 'ice sword' attack, which does
  - Store 0xFFFFFFFF in damage_to_deal
  - sleep(1)
  - Interprets damage_to_deal as a 64-bit integer, and deals that much damage.

So, by issuing a 'fireball' and then an 'ice sword', we could do -1 damage. Repeating this twice kills the final boss.

The attached script hunting.py automates our solution.
