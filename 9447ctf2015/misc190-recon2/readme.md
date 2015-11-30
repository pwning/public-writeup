## Recon 2 - Misc 190 Problem - Writeup by Robert Xiao (@nneonneo)

### Description

> Find the attackers full name. See attached file on Recon 1.

> The format of the flag is 9447{firstname.lastname}. It will be obvious when you've found the name. 

### Solution

Following on from Recon 1, we found our attacker's website at `dynamiclock.pw`.
`whois` yields little, and the site itself seems to be run via CloudFlare.

On the site, there's a contact form. We fill out the contact form and wait for
an email from William. The message header shows the real IP address:

    Received: from www.dynamiclock.pw (dynamiclock.pw [162.243.7.88])
        by ismtpd0006p1iad1.sendgrid.net (SG) with ESMTP id KCN0Sh5tQh6zFMmjd1yiag

Visit `162.243.7.88` and we get a plain directory listing with the following
files:

    [TXT]	dynamicWarl0ck.vcf	2015-11-16 02:24 	301 	 
    [IMG]	me.png	2015-11-15 03:51 	17K	 
    [TXT]	robots.txt	2015-11-15 03:35 	26 	 

`me.png` and `robots.txt` are pretty uninteresting. `dynamicWarl0ck.vcf` sounds
promising, but it doesn't have his last name. However, it does show that his
preferred Internet username is `dynamicWarl0ck`.

Googling for that name yields nothing. On a whim, we guess that he uses GitHub,
and go to http://github.com/dynamicWarl0ck. This user page says that he "moved
to bitbucket", so we follow along and go to
https://bitbucket.org/dynamicWarl0ck/, where we find a single repo:
https://bitbucket.org/dynamicWarl0ck/dynamics

In that repo, we look at the commit history, and one commit stands out:

    William Clutterbuck  committed 6361434

along with the text content

    nine four four seven lbrace william.clutterbuck rbrace

Therefore, the flag we want is `9447{william.clutterbuck}`.
