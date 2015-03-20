This challenge told us an organizer was giving away flags to people
that he trusts, and we were given a memory dump from a competitors computer.

Approach
--------
Our first approach was to run strings and get an idea for what is going on
in the memory dump. The main interesting thing we note is that Pidgin seems
to be running and connected to an IRC server. It appears the person whose
memory we have dumped was chatting with the organizer using OTR, an
encryption protocol for chat programs, based on strings like:

    acidburn88!acidburn88@9447-537D7FC2 PRIVMSG testicool69 :?OTR:AAMDKp5lWJgnAKoAAAAABAAAAAUAAADAfVDErkCfqT7yFV6ZHjgdTO5VEZw+z/v7kztd0RwYzDMMcGWl+17mBEGuV+2f6PpPuwcaJlGR5XczZbguNk6SJMGIfUFkJPZPn9rMe85zXyRZIVvJlXUQVfldCwVUR3thO8lo9BoRLMJqu2TmS4qEXGFx313+ELlH8jT1+yqjsA4pfH7CRzzQb7Hp0smmyAno96VGbjg7z/2vSqS59tn92cj0HDRpRygw5qP9E4k3P7Kb/HO7x4vWOABfcrt0qExZAAAAAAAAAAEAAAARUiRIRBG2NqWbFWmFUj2MNRuIQHP4Z8mfg2fJrM9bmhIXcrVn8QAAABQEZyB5JdUdZD9sCu+OrabwG3FFPw==


The first thing we tried doing was decrypting the chat. Although OTR has
Perfect Forward Secrecy, if the ephemeral encryption keys are still in
memory, we should be able to decode the conversation. Unfortunately, after
several attempts at this (searching for AES keys based on their key
schedule, and then just using every sequence of 8 bytes in memory as a
potential key) we were no closer to getting our flag.

After re-reading the challenge description, we realize maybe we are
taking the wrong approach. Instead of reading the message, we should try
to impersonate the competitor whose memory we have captured.

Implementation
--------------
The first thing we do is get a sample key for OTR with Pidgin. It looks 
something like

    (name "YOURACCOUNTINFOHERE")
    (protocol prpl-jabber)
    (private-key
     (dsa
      (p #00000...
      (q #00000...
      [etc]

So, we do a simple grep through our memory: `strings challenge.vmem | grep '(dsa ' -A 5 -B 5`

And we see the following:

    (privkeys
     (account
     (name "testicool69@yodawg.9447.plumbing")
     (protocol prpl-irc)
     (private-key 
      (dsa 
       (p #00FDAE11E35E2CC5B1E77F511DAFA9275AF4131D3FED6C62BDA7D769CB5DD087AE8958AC9D889738C01504368BAB424913B1D2D6C444B8F4302F2BA18398FC47AD21C857AC6A2F418AEDFB7438DF109F8FA993178F36C28B1317168236A818EEBF26F8B6622309F55A1AFF852635C7A91B7AF81611DD3A2D523D986DB796BD964F#)
       (q #00826BC3FA1959EC3673159500570F55A2AA536D65#)
       (g #098E7AD393E49BCD15109D8E18AC10592D72DBD66ECA2EAD9F51233CE56B8385794DD057EC0AFA73D3A17576A7BA8D856E7F727DD8F501C60B9D0FBAFA7DF5A62837A96A6F2F5EC5825A495FBBF0659FB3C90F8DE13ACB06028AFC46F6BD180ECBEBED2770804E6A29AF4410DA6B3E469823F859C676D284D54414BBFE7DE913#)
       (y #08E73F59BA6E993993204E6E573433DB5EDD2A9E10A0BD7262B03E73E6F5856B60BB909A8AAB780AA24004DB448E845545E65C06ED4C17D5D44661AC55EEC0B6AD80011F4D9A4356FE7A9550034B55AFB12B85F31AA1A6C252FA80C8DA3B62937AC0E41B991EDF312C20535A6022FEA16DC6BFFEC67731A767EFBCA1873C5621#)
       (x #3B078BBA7994F444245AC964C04B547B07FCEEAD#)

We install this key in our own system in the `~/.purple/otr.private_key`
file, and we add an account for `testicool69` on the irc server `yodawg.9447.plumbing`.

Then we try to talk to `acidburn88` and see if we can coax a key out
of him. For some reason this didn't work at first for us. In order to prevent
griefing the server disconnects CTF players logged in as `testicool69`
after a brief period. After a lot of messing around and eventually
restarting Pidgin we were able to start an encrypted session. Magically
`acidburn88` decided we were trust worthy, and sent us the key
(unencrypted for some reason):

    9447{forensics_champ!}
