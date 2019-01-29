## THE Matrix

We are given a gameboy ROM with the Matrix theme.

We used a gameboy emulator/debugger called BGB (http://bgb.bircd.org/#downloads), which allowed us to look into memory (or patch the code dynamically).



### 1. Catching the white rabbit

We are told to find the white rabbit, but as soon as we reach to it, our character (Neo) dies from a bullet. The game displays "Game Over" text and restarts from the beginning. When we look closer into the game code, we see that the game state is configured in two different ways based on the counter value in memory address (0xC402). Specifically, we can look at 0x4C37 to figure out that the counter needs to be 6 or greater to get into the different state.

This counter corresponds to the number of times Neo died. After the 6th death, the game resets but this time without codegate header and key checker screen. Morpheus now speaks about the red pill, and we have a different icon for Neo. When we catch the white rabbit this time, the bullet goes around and does not kill Neo.



### 2. Saving Morpheus

Now we are faced with Agent Smith, next to Morpheus. When we get to Agent Smith, we are told to "connect to the Matrix" and the game hangs. At this point, the game is waiting for the link protocol. Specifically, the game is receiving data and stores it at 0xC42B, which later gets compared to the value 0x64. If the correct value is set and 0xC42C contains the value of 0x00, then we can get out of the loop and continue. This action sets the value that later get validated.

When finally talking to Morpheus, he says that we need to find the key maker Architect. Then, the game prints out a series of numbers that corresponds to the values starting from 0xC414. This number has to match with "61111111".



### 3. Key Maker

Once we pass the above checks, we get to the key maker process. We just need to type in the keys as presented: "AAAAAABA", followed by the start key. If the key was entered correctly, the game just repeats to say that the answer is in the Matrix. This happens about 200 times and exits -- nothing happens afterwards.



At this point, we figured that the flag should be somewhere in memory. When we traced what memory was affected as we are going through above actions, we noticed that the memory contents starting from 0xC0C8 have been updated. It looked like some kind of sprite numbers (index). Following that data, we see something that resembles a bitmap data starting at 0xC230.

Using these two sets of data, we could write a simple script that will turn the sprite indices into the flag in a bitmap text.

Flag was `THERE_IS_NO_SPON`.

