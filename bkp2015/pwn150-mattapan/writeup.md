## Mattapan - Pwning 150 Problem - Writeup by Robert Xiao (@nneonneo)

The flag to Park Street was `OFPFC_ADD`, which could be found by some quick Googling and finding the OpenFlow specification document. (This flag was necessary to talk to the server).

In Mattapan, you get the chance to configure an OpenFlow switch which controls some traffic on some foreign network. Since I'm lazy, I just downloaded a Python package (`pox`) to act as the controller. The goal of the challenge is to configure the switch to do something to the traffic.

We start by simply getting the switch to copy packets back to the controller, one of the basic features of the OpenFlow protocol. This is achieved by a very simple Pox script (built by basically copy-pasting bits out of the forwarding examples):

    from pox.core import core
    import pox.openflow.libopenflow_01 as of
    from pox.lib.util import dpidToStr

    log = core.getLogger()


    def _handle_ConnectionUp (event):
        msg = of.ofp_flow_mod()
        msg.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("Hubifying %s", dpidToStr(event.dpid))

    def _handle_PacketIn (event):
        print event, repr(event.data), event.parsed

    def launch ():
        core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
        core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

        log.info("Test running.")

When we run this controller and point the switch at it, we see a packet dump of all the traffic, and in fact the flag (clearly denoted as `flag{...}`) is just among the traffic received: problem solved.