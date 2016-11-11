
# Trump likes Colors Writeup
### Writeup for HackTheVote 2016, 250 Points
@evandesantola  [evandesantola.com](evandesantola.com)


## Description
>Somebody leAked TrumP's favorite colors, looks like they used a really esoteric format. Some chiNese hacker named "DanGer Mouse" provided us the leak, getting this crucial info could really sway voters at the polls!"

## Initial Examination:
In this problem, we are given a large PNG file and the above prompt. 

![alt-text](images/trump_likes_colors_handout.png)

Opening the image in Preview, and reading the prompt with the conspicuously capitalized A, P, N and G, we discover that we have an APNG file.  Looking through some of the frames, we discover that we have a series of 16384 images with bars of different lengths.  We make the educated guess that the colors in these frames are encoding some sort of information, possibly alongside the time delay between each image.

After struggling for an embarassingly long hour to find a good way to either split or read in the images individually for use in a script, I finally download and use [APNGb](https://sourceforge.net/projects/apngasm/files/2.7/), a software that splits the images into their constituant frames in addition to creating text files that contain information about the time delay between each image.

After waiting for the images to process, we get a large folder full of 16,384 images and 16,383 text files.

Iterating through the files and comparing them with:

<`cmp --silent $first $second || echo "files are different"`>

We discover that all the intermediary files containing frame rate information are all identical and that these images are displayed at a constant frame rate. We assume that the only thing that is changing between frames is the changes between the images is the pixels within the images.

As there are 16384 frames (128*128), we hypothesize that the image likely corresponds to another image (with dimensions 128 by 128), whose pixels are encoded by the relative proportion of colors in the top right of our images.

## Implementation:

We iterate through the pixels of each frame and set a new image's pixels to be the relative color frequencies:

```python
if (pix[row,col]==(255,255,255,255)): 
	continue #Ignore black pixels
else:
	#Get the RGBA Value of the a pixel of an image
	rs+= pix[row,col][0]
	gs+=pix[row,col][1]
	bs+=pix[row,col][2] 
	# Set the RGBA Value of the image (tuple)
	
 pixels[i/128,i % 128]= (255*rs/(rs+bs+gs),
 	(255*gs/(rs+gs+bs)),(255*bs/(rs+gs+bs)))
```

Where we get:

![alt-text](images/results-trump-likes-colors.png)



Cleaning this image up, we see that in the above image, each bar has a unique height, and that there are approximately enough bars to make out the characters in a flag.  Additionally, each bar has a height on the range [0,128), suggesting to us that the height of each bar corresponds to an ASCII character.   Modifying our script, we get the height of each bar and its corresponding ASCII character with a script, with:

```python
t=""
for column in columnHeights:
	if (column!=127):
		t+= str(unichr(column))
print t
```

[Images and Code](/files/TrumpLikesColorsStuff.zip)

We get:

`flag{7h15_w45n7_3v3n_4_ch4ll3n63._54d_.}`

##Update:
So, I read the other writeups, and apparently there was an esolang that would have made this easier.  This has taught me to read the prompts more carefully in the future to look for even more clues.


