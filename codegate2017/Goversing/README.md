## Goversing – Reversing Challenge

Goversing was a Golang reversing challenge. The program allowed you to "login", and if your username and password passed a check you would be allowed to print out the flag (which appeared to be implemented as a SHA hash of the username and password; I didn't bother reversing that part because passing the username-password check was enough).

The gist of Goversing's username-password check was:

  * Apply some transformation to the input username.
    - This transformation produces 8 output bytes for each input byte.
  * Check the transformed username against 64 fixed bytes.
    - Just a memcmp-like check
    - Sets a fail flag if the buffers aren't equal
    - Also sets fail flag if there weren't 64 transformed input bytes
  * Apple some transformation to the input password.
    - This transformation was a 1-byte to 1-byte transformation.
    - I think it might have been just xor(input password, repeated input username)
  * Check the transformed password against 29 fixed bytes
    - Same fail-flag setting logic as above.

I'm not sure what the transformations were, but a bit of dynamic experimentation showed that they were character-by-character transformations and thus the checking logic is vulnerable to brute-forcing character-by-character.

The attached script go.py runs Goversing under gdb with breakpoints set inside of the memcmp-like checks to see how many bytes match. It does this repeatedly, searching for the inputs with the most matching bytes character-by-character.
