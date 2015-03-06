## Orient Heights - Crypto 250 Problem - Writeup by Robert Xiao (@nneonneo)

In this problem, we are given an implementation of the ElGamal signature scheme along with 357 putative signed messages.

The hint for the problem says

> Obviously, don't use one of the signatures I gave you---that still won't work.

So let's look at how they check for duplicates. In `asn1.py` they check for duplicates by putting all the raw (ASN.1-encoded) messages in a big list, and then rejecting your message if it appears in the list. Because they are operating on the raw encoded values, it may be possible to pass off a duplicate message if the encoding is different.

As it turns out through some experimentation, the ASN.1 parser ignores bytes past the end of the encoded message. Therefore, all we have to do is just append some garbage to a signed message -- the raw bytes will be different, but the message will decode to the same thing!

Now all that's left is to see if there's a correctly-signed message that contains what we want. As it turns out, `sig343.txt` contains a valid signature for the target message `There is no need to be upset`, and thus the attack is quite simply

    s.send(open('sigs/sig343.txt').read() + 'x')
