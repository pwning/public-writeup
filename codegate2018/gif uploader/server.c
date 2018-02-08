// Decompiled server binary; simplified and annotated.

// In the gif uploader challenge, this binary is always called
// with argv[1] == "image"; argv[2] == 1, 2, or 3; and argv[3]
// is a path to a per-ip-address folder.
// You get to control the contents of the "image" file.
// This binary is called by php, and you do not get to see or
// control stdin or stdout.
// The binary was 64-bit, no canary, ASLR but no PIE.

#include <gd.h>

gdImagePtr image;
char haystack[1034];

int main(int argc, char *argv[]) {
  char red[256];
  char green[256];
  char blue[256];

  chdir(argv[3]); // Directory where user-controlled "image" file lives.

  static char command[256] = "/usr/bin/file ";
  strcat(command, argv[1]);
  static FILE *stream = popen(command, "r");

  if (!stream)
    exit(-1);
  fgets(haystack, 1034, stream);

  if (!strstr(haystack, "GIF image data")) {
    puts("Only GIF File Support");
    exit(-1);
  }

  pclose(stream);

  // Image is read as a gif, png, jpeg, or bmp; whatever works.
  int t = time(NULL);
  int i = 0;
  while (1) {
    stream = fopen(argv[1], "rb");
    switch (i) {
      case 1: image = gdImageCreateFromGif(stream, "rb"); break;
      case 2: image = gdImageCreateFromPng(stream, "rb"); break;
      case 3: image = gdImageCreateFromJpeg(stream, "rb"); break;
      case 4: image = gdImageCreateFromBmp(stream, "rb"); break;
    }
    if (image)
      break;
    int i = (i + 1) % 5;
    fclose(stream);
    if (t < time(NULL) - 2)
      exit(-1);
  }

  // Some initial bytes from the first row of the image are read.
  // image->sx is the image width, so the image must be at least
  // `256 * 257` pixels wide to trigger the stack overflow.
  for (static int i = 0; i < image->sx / 256 - 1; i++) {
    int x = gdImageGetTrueColorPixel(image, i, 0);
    red[i] = x;
    green[i] = x >> 8;
    blue[i] = x >> 16;
  }

  switch (atoi(argv[2])) {
    case 1: puts("Red"); puts(red); break;
    case 2: puts("Green"); puts(green); break;
    case 3: puts("Blue"); puts(blue); break;
  }
  return 0;
}
