## Super Turbo Atomic GIF Converter - Web 180 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> Kids these days like fancy web video instead of gifs, so I made a converter.

> Flag is /home/ctf/flag.txt

> Find it at http://superturboatomicgifconverter.9447.plumbing:9447


### Solution

Looking at the source for this challenge, we see that it invokes `ffmpeg` to
convert the input file from GIF to WebM. However, the only validation it does on
the file is to check that the extension is `.gif`, and the file that is actually
passed to FFmpeg is a temporary file with no file extension.

Consequently, FFmpeg has to guess the file format from the contents of the file,
so we can upload things that are not GIFs.

FFmpeg supports certain meta file formats which are capable of including files.
The format I chose was HTTP Live Streaming, which can read local files using
`file://` protocol. Hence, we construct an HLS playlist and feed it to the gif
converter, which renders the contents of that text file as the WebM video.

See the attached `upload.gif` for more details. Upon submitting this file to
the uploader, the resulting video contains the flag.

### Flag

    9447{ffmpeg_m0re_like_ffRCE_amirite}
