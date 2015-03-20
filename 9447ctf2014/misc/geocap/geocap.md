This challenge gives us a pcap-ng file. Opening it up in Wireshark we see the
lyrics to the Pwnie-award-winning rap by geohot.

Approach
--------
The first thing to do is of course look through the TCP conversation for data
that is hidden steganographically. After staring at this for a few hours, we
find nothing. The lyrics match up perfectly, and there doesn't seem to be any
tricky things done with checksums or other fields in the packets.

After a while, we are given the hint "If you want a job done right, do it
yourself". Hmm...

At this point we start to wonder if Wireshark is lying to us. Perhaps there is
data in the packets that we can't see unless we write out own parser?!

Implementation
--------------
There are lots of ways that a parser for pcap-ng could be written, but we chose
to use the trusty hex-editor [010editor](http://www.sweetscape.com/010editor/).

This allows us to write templates for certain file types to help in
understanding and parsing them. Opening up [documentation](http://www.winpcap.org/ntar/draft/PCAP-DumpFileFormat.html)
for the file format, we can start to write our own parser.

After getting the basic structure down, we open up the file in 010editor and
take a look. At first the packets look exactly as they appear in Wireshark--
there isn't any data missing from the packets. However, we quickly notice
something odd: there are packets with a `block type` of `9447`.

We take all the data from these blocks and concatenate them together and 
end up with a gzipped blob of data. Unzipping them gives us our flag, and 
geohot's catch phrase:

    9447{UHHHHH_KEEP_HACKING_ELITE}
