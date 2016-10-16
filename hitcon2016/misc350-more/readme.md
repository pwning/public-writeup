## moRE - Misc 350 Problem

### Description

We're asked to connect to a remote service which challenges us to solve a series of challenges with regex.

This is similar to [RegExpert](../misc200-regexpert/readme.md), but the challenges are even harder.

### Solution

As with RegExpert, they are using the Ruby regex engine.

#### 1

> ============== [Leap Year] ==============
> Even my cat can code this 🐱
> 
> 82 byte limit

A leap year is any year which is `divisible by 4 && (not divisible by 100 || divisible by 400)`.

A number is divisible by 4 if the last two digits are divisible by 4. We code a little expression to find all numbers divisible by 4 and not divisible by 100 (ending in 00):

    (.*0)?(4|8)|(.*)([13579][26]|[2468][048])

Then, we OR this with any year divisible by 4, which is simply all years ending in 00 with the preceding two digits divisible by 4:

    <the above constraint>00|0|.*0000

Reject numbers with leading zeros `(?!0+\d)`, and then require every match to consist of only digits, to get the final result:

    ^(?=(((.*0)?(4|8)|(.*)([13579][26]|[2468][048]))|\g<2>00|0|.*0000)$)(?!0+\d)\d+$

#### 2

> =============== [x^(n^2)] ===============
> 
> We like squares: ■ □ ▢ ▣ ▤ ▥ ▦ ▧ ▨ ▩ ▪▫
>
> 16 byte limit

The idea is very simple: match any string that has 1, 1+3, 1+3+5, 1+3+5+7, ... `x`s. The classic solution is

    ^(^x|\1xx)+$

which rebinds `\1` each time to add two more `x`s. However, Ruby's engine wants a slightly different syntax:

    (^x|\k<1+0>xx)+$


#### 3

> =========== [Multiple of 42] ============
> 
> The answer to life the universe and everything.
>
> 725 byte limit

This is just ugly state machine crap. Basically, match any string with a length divisible by 2, 3 and 7 simultaneously.

2 and 3 are fairly easy (2 is just `.*[02468]`, and 3 is just walking through each char flipping through a state machine), but 7 is nasty. We just got a nice short version off [codegolf.stackexchange.com](http://codegolf.stackexchange.com/a/3518/6699) (cudos to @Lowjacker), and pasted it in for the win.

    ^(?!$)-?(?!0.)(?=.*[02468]$)(?=([0369]|[258][0369]*[147]|[147]([0369]|[147](?<K>[0369]*[258]))*[258]|[258]\g<K>([0369]|[147]\g<K>)*[258]|[147]([0369]|[147]\g<K>)*[147][0369]*[147]|[258]\g<K>([0369]|[147]\g<K>)*[147][0369]*[147])*$)(?>(|(?<B>4\g<A>|5\g<B>|6\g<C>|[07]\g<D>|[18]\g<E>|[29]\g<F>|3\g<G>))(|(?<C>[18]\g<A>|[29]\g<B>|3\g<C>|4\g<D>|5\g<E>|6\g<F>|[07]\g<G>))(|(?<D>5\g<A>|6\g<B>|[07]\g<C>|[18]\g<D>|[29]\g<E>|3\g<F>|4\g<G>))(|(?<E>[29]\g<A>|3\g<B>|4\g<C>|5\g<D>|6\g<E>|[07]\g<F>|[18]\g<G>))(|(?<F>6\g<A>|[07]\g<B>|[18]\g<C>|[29]\g<D>|3\g<E>|4\g<F>|5\g<G>))(|(?<G>3\g<A>|4\g<B>|5\g<C>|6\g<D>|[07]\g<E>|[18]\g<F>|[29]\g<G>)))(?<A>$|[07]\g<A>|[18]\g<B>|[29]\g<C>|3\g<D>|4\g<E>|5\g<F>|6\g<G>)$

#### 4

> ============= [Complement] ==============
> 
> Please match x,~x where x is a binary string. Like "0,1" or "1001,0110".
> 
> 63 byte limit

The approach is simply to match any string where any pair of corresponding bits are *equal*, then negate the expression.

Make an expression that matches `.{n}0.+,.{n}0` (using recursion):

    (0.*,|.\g<1>.)0

OR on a similar expression that matches `.{n}1.+,.{n}1`, and you get an expression that matches the string any time corresponding bits are *equal*.

Negating all such strings, then restricting the format to `[01]{n},[01]{n}` with

    (,|[01]\g<1>[01])

finishes the problem.

    ^(?!,|(0.*,|.\g<1>.)0|(1.*,|.\g<2>.)1)(,|[01]\g<3>[01])$

### Flag

After solving these four challenges, you get the following message:

> Congratz! You are now our CRO (Chief Regular Officer).
> 
> ATTENTION! HUGE GIFT IS COMING!
> 
> 3...2...1...
> 
>     ^([[dKSbqJWjnuhQ}iyfspkUPY HBFxtRE{GCLOXwoNcv]&&[^dqEpDvkz\-}BPoIrXFW ]&&[^Oo zE}PvdBl\-:DkcUXifjnLMueryg]&&[^EmlpD}TYbiaNonudjHAwzCUcQkxf{vSWFrXgIOBV]&&[f:VLxUeGFYMEoaWyPchBbvA]&&[^XsZjFxQ:wAgqiE{er\-fODTd]&&[^EtZlYUze\-G{JgyVcfknDSXCRo:jx]])([[srkgOMniDpXEujfdVwBYUKJmWAQ{Sqh\-oRa b]&&[IVyWRAJBxiGkDoefLQt]&&[^Y:PsuMK br{mjZkgG]&&[^KVcqnRYdojLQXsrBlzeyDI gbStGZ]&&[ ZEMnjAbkH{iQKmzgDtTsFpxXI:uCvfUVdqSlBwYP]&&[^qsbGCEn:NFDhyU{]&&[^}\-zWEAOTJSMrIaPHChvN{Y]&&[tvYkLJrTiAxeVnHmjQ I{FpRqESyzONlKCWg\-cX]])([[^Ssk}\-mqKUOARXIuZLgDpHeM]&&[OFxcVeqJHbtYvmuza]&&[jKHYwgPpsntbkCdl\-UxBTZFaVGzSOrvem]&&[^gKyqRLDMcA kWmlHEJGPXSdxeZ\-F:sobz}rC]&&[pRwAFqeKc{jnzU ClmNOhiYWPxytVbufX:GTg]&&[^zmUMVNk}SWCiDGLFTP:Xsea\-]&&[\-QVjC:woRJtFAvkIbEKGYi{DLaxf]&&[PVcx wFZNuklmqbzshpedGf}tWSaTXo\-OiL]])([[^xNFB:TzpysbwA ]&&[^wyNXgCKLTMIbAtRU]&&[^eGIdM SroOjLpDVNatWA\-JKqCwU]&&[xUEnXRGLmCHkdTMuBZeSqc}yh:IpwlQA]&&[TC\-pUB{xIlH:sPaKvkoDQeAXiMWnJNGVrLy hFR}cS]&&[BFVabZicAu sEqmLxdTP]])([[td\-{kaP iEFWqCZlOomnSVeG}]&&[mAzYtkBZjEH oWligRncIhNs}]&&[vYeb\-VAg:oQSRwjMkd]&&[IPgS}kr DiazyxudVHneNsEcmoQRBtbMGKhWq]&&[QNkdSTWKF vBoqPXJrItayA]&&[aPL{AQ:RJ\-fFrETKel}unxpYBmVq vwoSOdUIbCjtH]])([[^Xm fQlHLDeGJtwqgCTxAB]&&[^Odhsi{lPbyotmRFkzHcAf XEIuGVKYaeUWJwgjZpM]&&[^FgG}sPyXEdTwWxvcrCUjN:\-M]&&[^abJd\-IFyWeEixGM{V:ATrOqLposcvNU ]&&[ukRGnoW VBK}yq]])([[nzK{aRQwqYIsZvuMxyO:GUFWb\-lrSc]&&[DULOQ{IxBgRAhymMJe]&&[^tuEybwanKZhJOVlUQ\-ioRM XfvqP:NrdcIDzAxeH]])([[PujVDm:fOxEygG{sIbJkRnrC\-}HSaUlXdMBZLYio]&&[^MiWlhQtrfDodTHGS]&&[RzwgjWbda}SDUcXHfBAos{mI\-lQOtYJ]&&[^vZQBsXYo{VxjCpFyD]&&[\-emjNSv:LPkVta}IoTzdYGKCDq{fQnJhRybUZAOF]&&[iHPGNJkaScdY:BtIRVmXOw}M]&&[Z RkohALFygUut}NYdmGQprEeIWwxqs]&&[nDUCkRQLlqTPHstyhxoA\-Guap]])([[^T\-DkmjSx{zGO CLB:FZEiIVKUfqH]&&[JbR qf:ey{jQOrVBM]&&[BHQcfZr:iyovVLPJRptgM}FGX{neSulwT]&&[^Pag}fD:vu LHdRoYshziXTQFmpZCtlwG]&&[vL fI{iYMHbj:NVDck\-ZeRUQ}PqBTpAuhFCGKJsO]&&[^SpOVGYWwKZHsravMnIkDci:uogPjAXxBCUfbqRQEy]&&[^VIEGU:jvyhQw{xsioSgWTdPDcZrJRB\-HLKOA}lmzM]])([[YOepxMTni{sFR UdlkhtJrKo:ZDHXEzASgGVf]&&[zXJlpWqfhswme{vUVd\-ZL}KQoItyYSbaR:OGE]&&[^EpAWqdDONwLTtCkm ZMsy]&&[^kpd\-nASNDaLvWhmMyEeYJoHjGOTziX{IF l]&&[^bse{rtKxY\-kyOd]&&[^QKMdVsRvaq}AyCHneglrXDTcSo{UIbZFNOj]&&[ivfpnNSbIROhCj\-MDuwygazmqxoPL:KGAc]&&[GnCOM}DsfxoBSUzHItXFQiPEpVbdkq:hRcTJLeg]&&[^hDtfnY\-KZgRLSFz]])([[JYOmFnZCMyLoQGNXz}kUgDdW A{wscevhbIRqSE]&&[^aJdQXmlVHroTfw]&&[^vzeKuJiFGST\-cDm jVqCdNy:]&&[^kDLtoJsfixvMXpVE SBRd\-AU:lQuqP}cYn]&&[^jeAMXfFpBlYO dWgShJRqv}TUNCbkzP]&&[qwGYZmefjtJNbL:gyuiKPsMn}BprTDIkRFocvx]&&[^tMI:U}uzkK\-Ogad]])\9([[^tAjm\-WcNe{STqiwlEfPhQ}:nXoCkxFu]&&[gmvMKIUSAFXxaEd{\-N bwo:RGCkeyVQrPOqlcD}u]&&[gJx u:YONUlbM{CKrocsk]&&[gJHCARb\-Z WnfTGzjp:MhYaFseVwSrli]&&[^}GUxR{yKl\-AfMXiFOYNHkw]&&[^xAUOIVozPv\-gQJsjLSe]&&[^U}QipGex{quvHDZ JA]&&[^YRFsayHbzjQ:CL\-tDxlpN]])\5([[S\-kYJaogmdW{cVK}AFCsnf Irqile:X]&&[fBQFUpGkInrVHS{JCujcwM ZiL}\-RWvdy]&&[u\-PnYjdrtB colfQHOIDKSbZUiJ{]&&[^E}uHVzplmiIvaFCZksy:AnWMeo]&&[^gmu}\-eJXlTqIZL]&&[zKVJgdFDEvcLksjYBHmGRWTiPlwMOSXC :bt}Z]&&[URKEWj\-qx{ekAglQ:DozcaMtHsB hPFCYZu]&&[^ARlmN}TuUZ{fFhsX:iJ]&&[^LVdTwsPjaRQGpJYcXeMHuxEBZ{q\-kKlFWmtg]])([[^TeW{vc}rJCqVgyHOPZpwM]&&[^xnevtzrilpJXHISOTdGCumAwqEsU]&&[hTFAEIaNMuyXHe:QiSr\-fLm}vbYUD{RkJBgKq x]&&[XCLNRxtPivVnhBKu\-olwpYsEWzkUMqaeGT{]&&[kCVXKEPwQWDh{qYmBOgZUlIaRHN:jJv\-bTxMncs ]&&[^dQqWLhNBmjCtoOYyGTSMFzVRli}rvHgkA ]&&[^{dUaK}t:gLFlfVEeTvmCNIxqZYijnJokspWcAHbSX]])([[^wEaDvpNlILVQAXGu]&&[^rDnApNtPmeVUuLoJQ}FRBKwqy O]&&[^\-eE:YlaJk}yRoLWugzdVZPT MDvrqHUGn]&&[^n}zejcgb{Gsfk\-J NaiolwEYWDHdLTM:VmyXAvpQq]&&[nckSa}mzWJU:BxPwltY{TVMsvXpoGeiOI]&&[akS\-Iy}mvL{lWU:GNDHQKYATCsErdgpzOM wX]])\3([[^}KWdlCNqGHBjJhsDIMrAEp]&&[^mFnOYG iXrjVdT]&&[^E B\-AzxKQX{SyvJb:gIRqkdUhtNG]&&[u{noSO}Kg\-WDYp:javyV]&&[^eHBZVpkxUFCw:f]&&[ WPRGxOuBimLkYc:wsadqf}lyJzvDUnNAQKbVIj\-e]&&[JNwKD{aUoie qEyWrpPkZBFTh]])\12\3\2\6([[aHcCmUkIfQtVgEGl hxYXFiuKeSLZ]&&[xefFIqAgSaYMuGs]&&[^uGLnsoDclFqhIQbfvOWix{ezHJV aZ:ytUpmYTw]&&[ITtQmBnJSUgNDV}hAWXGMsureERFL]&&[^ldLBEXwC{tP H:zyIKODU]&&[^OEVYTbFq hHed\-KcXw]&&[^SxtJGvPc\-XDFKRsYZanur]])\13([[wLPkKCduRy\-aMOlmbiFEZWXvIGJjoDct]&&[EDrC}I{xBT\-hcabNusAPFneqJOX:ki j]&&[xiFIYQMDLGHlmV{a\-XyZP]&&[^uG s}XCzqnTKBvH]&&[nzLdajUB{CmwySsAROk\-QKFPMxftv}olDi]&&[^DjqEMzyRhuSZJxbWQsLvONUCG Vfk:KmdYaw\-TnitH]&&[Qd{PUywXOpxzurml]])\12\5\17\12\16([[PBr{mqMZFhUazHpOxKSfondtV}TkICRbLGg:yD]&&[joDyrlszYQNUcSfhmVnPuEHb]&&[A:DBcWzNsnmX JCLTaxOVSH}fYZqro]&&[x:nR{DMCNGKlAqSvemziYufHFw dc}ZsLkQbWryh]&&[WrHQ\-EezlgLwNPT}pUCFicMoa:jtDfmXbyRB]&&[rsIwzLy{HVCKtkAndxOlRF TXmNZQafjBUPGJ:pMc}]&&[^CUtQDsIjhNF \-nlpiAVHuBRYEoKXdwS{yLaGf]&&[kYphKuSL}emn{wxOVTrCNJHoIfUavXAD]&&[{oIxVNXZHiM\-AwcjsdCOtmFzB]])\19\2\6\17\13\2\6\13([[LC Awgo:OBe\-hNTtuKaSbqzlcG]&&[^FxTbDHLga}UWjyOtXh\-RqeMzdflPVJnImBYkCiN]&&[mkOlsoBhb:{TiuNPeHqLnY}MgZ\-UfAvQz]&&[^r\-dOsbDVPcyiSwUXRh FoCLWIvQuza]&&[^bVJUOwlNjPdzBCeZa{GkHEgWchr]&&[REg{W oUv:VnmwAXa]&&[^rnqgfEcmetLih}JKUbTZW ON]&&[^NxDRsYGZyjatCoqXPWr]&&[^WkXcKVYSjTf{ydnupPUbwqtMGJhONQRv}DHg:ei L]])\6\5\3\1\9\12\13([[Ay MDBhsCnWTGfrcoqF}N\-ZUQixmRkzbpYud]&&[^GENTDZQe\-PnVxIdJAMBjOcCz:Xp FyHbgRraf]&&[znksUoR:JjEDBpSNChQWZ f}OYiwugXA\-y]&&[^YQZPzcVluyn}qe:SDBbtIUNd iO{r]&&[^UEGPoLdriVzNglYmyObTnv :]&&[^UYdtg{PbaZHOjlFi:rQycEIvVBx\-sADCLS}R]&&[^hON{U\-lbyEJASYLoGD]&&[osuJSiHrN{htdUDGaZWPImM:FBQ bYOA]])\5\12([[^EVFSeGNrbDCaM{KmLh\- YHdopOsInfXW}]&&[^XGSh}Ha:eADCPpcEZrjidzOMBUImwQWon sL]&&[v{dOApXUfG}haeqS\-DJyW:KHNoTzElkgYiImVFBucC]&&[^MmPebn:Q KhsDz]&&[^Kuog {OPQXivtTWzhDC}GSfcM\-k:wLAY]&&[FQiLqbSJwesUhf DuARlZdaIGg]&&[^FOLsfqRUIcCV{jJYmodivN}xAHPpy]])([[^CX:OBWnHboDhzi}F]&&[nrpgbcqI lTCQAowdZfmEGKyij:tPHhDU]&&[^sgLvMFGSR{quCTpBQKcProyA]&&[^mF:ZAoskhfgKwH]&&[MqiJYyR:SWDQpd v}rKwsmEcXHTzZtgakf{Gju]&&[^Ko\-psGakrVg:nYAiuFSxEXwbmehOM qNHURT]&&[cRydhm{iQDKaTvFeIAnBqWlwLt:GOs]&&[^lpgFNLIDZJKuzXT:Pf]&&[TzUePJX{\-ausnEicyWwdA}rIVRgMHNLQ:kKbDxSh]])\14([[^eSwrLVByhniCQvDsAcIlxfmNUWuMzToHKpGd]&&[}vNOcwzmipquLHtJah:rTfyZXl KBGCMSbUYe]&&[^kWsTvGqrV\-mfMac]&&[^ZLmIfqdnjCzRXrQYsbBWv\-UJ:plu]&&[jOV}CaWBkMKuFvcESLhsilz{YNydmfQRUXDxJ:ZtP]&&[jLzqHRo{:kabdrK}ZUsQCGiuA\-mecExvgShwMFJOyt]&&[EtRYlumkyHDUTz:Ve}i\-nBJdcOqKZpWXNFbxShfs]&&[^IxRqKplz:fYoerTn uCMDiJVyNUAQE]&&[^z{AqXkswgMfaJdOIN:PjytRebU]])$

What a lovely regex! It's actually very simple in structure: it uses Ruby's extended character class syntax `[[...]]` to intersect a bunch of character class sets (using `[[...]&&[...]&&[...]]` syntax).

I used my text editor's regex-powered find-and-replace to transform the flag regex into Python set intersection expressions:

```
s = [None]
out = ''
def add(x):
    global s, out
    x = x.pop()
    s.append(x)
    out += x
def backref(x):
    global s, out
    out += s[x]
def mkset(x):
    x = x.replace("\-", "-")
    if x[0] == '^':
        return set(map(chr, xrange(0, 256))) - set(x)
    else:
        return set(x)

add(mkset("dKSbqJWjnuhQ}iyfspkUPY HBFxtRE{GCLOXwoNcv") & mkset("^dqEpDvkz\-}BPoIrXFW ") & mkset("^Oo zE}PvdBl\-:DkcUXifjnLMueryg") & mkset("^EmlpD}TYbiaNonudjHAwzCUcQkxf{vSWFrXgIOBV") & mkset("f:VLxUeGFYMEoaWyPchBbvA") & mkset("^XsZjFxQ:wAgqiE{er\-fODTd") & mkset("^EtZlYUze\-G{JgyVcfknDSXCRo:jx"))
add(mkset("srkgOMniDpXEujfdVwBYUKJmWAQ{Sqh\-oRa b") & mkset("IVyWRAJBxiGkDoefLQt") & mkset("^Y:PsuMK br{mjZkgG") & mkset("^KVcqnRYdojLQXsrBlzeyDI gbStGZ") & mkset(" ZEMnjAbkH{iQKmzgDtTsFpxXI:uCvfUVdqSlBwYP") & mkset("^qsbGCEn:NFDhyU{") & mkset("^}\-zWEAOTJSMrIaPHChvN{Y") & mkset("tvYkLJrTiAxeVnHmjQ I{FpRqESyzONlKCWg\-cX"))
add(mkset("^Ssk}\-mqKUOARXIuZLgDpHeM") & mkset("OFxcVeqJHbtYvmuza") & mkset("jKHYwgPpsntbkCdl\-UxBTZFaVGzSOrvem") & mkset("^gKyqRLDMcA kWmlHEJGPXSdxeZ\-F:sobz}rC") & mkset("pRwAFqeKc{jnzU ClmNOhiYWPxytVbufX:GTg") & mkset("^zmUMVNk}SWCiDGLFTP:Xsea\-") & mkset("\-QVjC:woRJtFAvkIbEKGYi{DLaxf") & mkset("PVcx wFZNuklmqbzshpedGf}tWSaTXo\-OiL"))
add(mkset("^xNFB:TzpysbwA ") & mkset("^wyNXgCKLTMIbAtRU") & mkset("^eGIdM SroOjLpDVNatWA\-JKqCwU") & mkset("xUEnXRGLmCHkdTMuBZeSqc}yh:IpwlQA") & mkset("TC\-pUB{xIlH:sPaKvkoDQeAXiMWnJNGVrLy hFR}cS") & mkset("BFVabZicAu sEqmLxdTP"))
add(mkset("td\-{kaP iEFWqCZlOomnSVeG}") & mkset("mAzYtkBZjEH oWligRncIhNs}") & mkset("vYeb\-VAg:oQSRwjMkd") & mkset("IPgS}kr DiazyxudVHneNsEcmoQRBtbMGKhWq") & mkset("QNkdSTWKF vBoqPXJrItayA") & mkset("aPL{AQ:RJ\-fFrETKel}unxpYBmVq vwoSOdUIbCjtH"))
add(mkset("^Xm fQlHLDeGJtwqgCTxAB") & mkset("^Odhsi{lPbyotmRFkzHcAf XEIuGVKYaeUWJwgjZpM") & mkset("^FgG}sPyXEdTwWxvcrCUjN:\-M") & mkset("^abJd\-IFyWeEixGM{V:ATrOqLposcvNU ") & mkset("ukRGnoW VBK}yq"))
add(mkset("nzK{aRQwqYIsZvuMxyO:GUFWb\-lrSc") & mkset("DULOQ{IxBgRAhymMJe") & mkset("^tuEybwanKZhJOVlUQ\-ioRM XfvqP:NrdcIDzAxeH"))
add(mkset("PujVDm:fOxEygG{sIbJkRnrC\-}HSaUlXdMBZLYio") & mkset("^MiWlhQtrfDodTHGS") & mkset("RzwgjWbda}SDUcXHfBAos{mI\-lQOtYJ") & mkset("^vZQBsXYo{VxjCpFyD") & mkset("\-emjNSv:LPkVta}IoTzdYGKCDq{fQnJhRybUZAOF") & mkset("iHPGNJkaScdY:BtIRVmXOw}M") & mkset("Z RkohALFygUut}NYdmGQprEeIWwxqs") & mkset("nDUCkRQLlqTPHstyhxoA\-Guap"))
add(mkset("^T\-DkmjSx{zGO CLB:FZEiIVKUfqH") & mkset("JbR qf:ey{jQOrVBM") & mkset("BHQcfZr:iyovVLPJRptgM}FGX{neSulwT") & mkset("^Pag}fD:vu LHdRoYshziXTQFmpZCtlwG") & mkset("vL fI{iYMHbj:NVDck\-ZeRUQ}PqBTpAuhFCGKJsO") & mkset("^SpOVGYWwKZHsravMnIkDci:uogPjAXxBCUfbqRQEy") & mkset("^VIEGU:jvyhQw{xsioSgWTdPDcZrJRB\-HLKOA}lmzM"))
add(mkset("YOepxMTni{sFR UdlkhtJrKo:ZDHXEzASgGVf") & mkset("zXJlpWqfhswme{vUVd\-ZL}KQoItyYSbaR:OGE") & mkset("^EpAWqdDONwLTtCkm ZMsy") & mkset("^kpd\-nASNDaLvWhmMyEeYJoHjGOTziX{IF l") & mkset("^bse{rtKxY\-kyOd") & mkset("^QKMdVsRvaq}AyCHneglrXDTcSo{UIbZFNOj") & mkset("ivfpnNSbIROhCj\-MDuwygazmqxoPL:KGAc") & mkset("GnCOM}DsfxoBSUzHItXFQiPEpVbdkq:hRcTJLeg") & mkset("^hDtfnY\-KZgRLSFz"))
add(mkset("JYOmFnZCMyLoQGNXz}kUgDdW A{wscevhbIRqSE") & mkset("^aJdQXmlVHroTfw") & mkset("^vzeKuJiFGST\-cDm jVqCdNy:") & mkset("^kDLtoJsfixvMXpVE SBRd\-AU:lQuqP}cYn") & mkset("^jeAMXfFpBlYO dWgShJRqv}TUNCbkzP") & mkset("qwGYZmefjtJNbL:gyuiKPsMn}BprTDIkRFocvx") & mkset("^tMI:U}uzkK\-Ogad"))
backref(9)
add(mkset("^tAjm\-WcNe{STqiwlEfPhQ}:nXoCkxFu") & mkset("gmvMKIUSAFXxaEd{\-N bwo:RGCkeyVQrPOqlcD}u") & mkset("gJx u:YONUlbM{CKrocsk") & mkset("gJHCARb\-Z WnfTGzjp:MhYaFseVwSrli") & mkset("^}GUxR{yKl\-AfMXiFOYNHkw") & mkset("^xAUOIVozPv\-gQJsjLSe") & mkset("^U}QipGex{quvHDZ JA") & mkset("^YRFsayHbzjQ:CL\-tDxlpN"))
backref(5)
add(mkset("S\-kYJaogmdW{cVK}AFCsnf Irqile:X") & mkset("fBQFUpGkInrVHS{JCujcwM ZiL}\-RWvdy") & mkset("u\-PnYjdrtB colfQHOIDKSbZUiJ{") & mkset("^E}uHVzplmiIvaFCZksy:AnWMeo") & mkset("^gmu}\-eJXlTqIZL") & mkset("zKVJgdFDEvcLksjYBHmGRWTiPlwMOSXC :bt}Z") & mkset("URKEWj\-qx{ekAglQ:DozcaMtHsB hPFCYZu") & mkset("^ARlmN}TuUZ{fFhsX:iJ") & mkset("^LVdTwsPjaRQGpJYcXeMHuxEBZ{q\-kKlFWmtg"))
add(mkset("^TeW{vc}rJCqVgyHOPZpwM") & mkset("^xnevtzrilpJXHISOTdGCumAwqEsU") & mkset("hTFAEIaNMuyXHe:QiSr\-fLm}vbYUD{RkJBgKq x") & mkset("XCLNRxtPivVnhBKu\-olwpYsEWzkUMqaeGT{") & mkset("kCVXKEPwQWDh{qYmBOgZUlIaRHN:jJv\-bTxMncs ") & mkset("^dQqWLhNBmjCtoOYyGTSMFzVRli}rvHgkA ") & mkset("^{dUaK}t:gLFlfVEeTvmCNIxqZYijnJokspWcAHbSX"))
add(mkset("^wEaDvpNlILVQAXGu") & mkset("^rDnApNtPmeVUuLoJQ}FRBKwqy O") & mkset("^\-eE:YlaJk}yRoLWugzdVZPT MDvrqHUGn") & mkset("^n}zejcgb{Gsfk\-J NaiolwEYWDHdLTM:VmyXAvpQq") & mkset("nckSa}mzWJU:BxPwltY{TVMsvXpoGeiOI") & mkset("akS\-Iy}mvL{lWU:GNDHQKYATCsErdgpzOM wX"))
backref(3)
add(mkset("^}KWdlCNqGHBjJhsDIMrAEp") & mkset("^mFnOYG iXrjVdT") & mkset("^E B\-AzxKQX{SyvJb:gIRqkdUhtNG") & mkset("u{noSO}Kg\-WDYp:javyV") & mkset("^eHBZVpkxUFCw:f") & mkset(" WPRGxOuBimLkYc:wsadqf}lyJzvDUnNAQKbVIj\-e") & mkset("JNwKD{aUoie qEyWrpPkZBFTh"))
backref(12)
backref(3)
backref(2)
backref(6)
add(mkset("aHcCmUkIfQtVgEGl hxYXFiuKeSLZ") & mkset("xefFIqAgSaYMuGs") & mkset("^uGLnsoDclFqhIQbfvOWix{ezHJV aZ:ytUpmYTw") & mkset("ITtQmBnJSUgNDV}hAWXGMsureERFL") & mkset("^ldLBEXwC{tP H:zyIKODU") & mkset("^OEVYTbFq hHed\-KcXw") & mkset("^SxtJGvPc\-XDFKRsYZanur"))
backref(13)
add(mkset("wLPkKCduRy\-aMOlmbiFEZWXvIGJjoDct") & mkset("EDrC}I{xBT\-hcabNusAPFneqJOX:ki j") & mkset("xiFIYQMDLGHlmV{a\-XyZP") & mkset("^uG s}XCzqnTKBvH") & mkset("nzLdajUB{CmwySsAROk\-QKFPMxftv}olDi") & mkset("^DjqEMzyRhuSZJxbWQsLvONUCG Vfk:KmdYaw\-TnitH") & mkset("Qd{PUywXOpxzurml"))
backref(12)
backref(5)
backref(17)
backref(12)
backref(16)
add(mkset("PBr{mqMZFhUazHpOxKSfondtV}TkICRbLGg:yD") & mkset("joDyrlszYQNUcSfhmVnPuEHb") & mkset("A:DBcWzNsnmX JCLTaxOVSH}fYZqro") & mkset("x:nR{DMCNGKlAqSvemziYufHFw dc}ZsLkQbWryh") & mkset("WrHQ\-EezlgLwNPT}pUCFicMoa:jtDfmXbyRB") & mkset("rsIwzLy{HVCKtkAndxOlRF TXmNZQafjBUPGJ:pMc}") & mkset("^CUtQDsIjhNF \-nlpiAVHuBRYEoKXdwS{yLaGf") & mkset("kYphKuSL}emn{wxOVTrCNJHoIfUavXAD") & mkset("{oIxVNXZHiM\-AwcjsdCOtmFzB"))
backref(19)
backref(2)
backref(6)
backref(17)
backref(13)
backref(2)
backref(6)
backref(13)
add(mkset("LC Awgo:OBe\-hNTtuKaSbqzlcG") & mkset("^FxTbDHLga}UWjyOtXh\-RqeMzdflPVJnImBYkCiN") & mkset("mkOlsoBhb:{TiuNPeHqLnY}MgZ\-UfAvQz") & mkset("^r\-dOsbDVPcyiSwUXRh FoCLWIvQuza") & mkset("^bVJUOwlNjPdzBCeZa{GkHEgWchr") & mkset("REg{W oUv:VnmwAXa") & mkset("^rnqgfEcmetLih}JKUbTZW ON") & mkset("^NxDRsYGZyjatCoqXPWr") & mkset("^WkXcKVYSjTf{ydnupPUbwqtMGJhONQRv}DHg:ei L"))
backref(6)
backref(5)
backref(3)
backref(1)
backref(9)
backref(12)
backref(13)
add(mkset("Ay MDBhsCnWTGfrcoqF}N\-ZUQixmRkzbpYud") & mkset("^GENTDZQe\-PnVxIdJAMBjOcCz:Xp FyHbgRraf") & mkset("znksUoR:JjEDBpSNChQWZ f}OYiwugXA\-y") & mkset("^YQZPzcVluyn}qe:SDBbtIUNd iO{r") & mkset("^UEGPoLdriVzNglYmyObTnv :") & mkset("^UYdtg{PbaZHOjlFi:rQycEIvVBx\-sADCLS}R") & mkset("^hON{U\-lbyEJASYLoGD") & mkset("osuJSiHrN{htdUDGaZWPImM:FBQ bYOA"))
backref(5)
backref(12)
add(mkset("^EVFSeGNrbDCaM{KmLh\- YHdopOsInfXW}") & mkset("^XGSh}Ha:eADCPpcEZrjidzOMBUImwQWon sL") & mkset("v{dOApXUfG}haeqS\-DJyW:KHNoTzElkgYiImVFBucC") & mkset("^MmPebn:Q KhsDz") & mkset("^Kuog {OPQXivtTWzhDC}GSfcM\-k:wLAY") & mkset("FQiLqbSJwesUhf DuARlZdaIGg") & mkset("^FOLsfqRUIcCV{jJYmodivN}xAHPpy"))
add(mkset("^CX:OBWnHboDhzi}F") & mkset("nrpgbcqI lTCQAowdZfmEGKyij:tPHhDU") & mkset("^sgLvMFGSR{quCTpBQKcProyA") & mkset("^mF:ZAoskhfgKwH") & mkset("MqiJYyR:SWDQpd v}rKwsmEcXHTzZtgakf{Gju") & mkset("^Ko\-psGakrVg:nYAiuFSxEXwbmehOM qNHURT") & mkset("cRydhm{iQDKaTvFeIAnBqWlwLt:GOs") & mkset("^lpgFNLIDZJKuzXT:Pf") & mkset("TzUePJX{\-ausnEicyWwdA}rIVRgMHNLQ:kKbDxSh"))
backref(14)
add(mkset("^eSwrLVByhniCQvDsAcIlxfmNUWuMzToHKpGd") & mkset("}vNOcwzmipquLHtJah:rTfyZXl KBGCMSbUYe") & mkset("^kWsTvGqrV\-mfMac") & mkset("^ZLmIfqdnjCzRXrQYsbBWv\-UJ:plu") & mkset("jOV}CaWBkMKuFvcESLhsilz{YNydmfQRUXDxJ:ZtP") & mkset("jLzqHRo{:kabdrK}ZUsQCGiuA\-mecExvgShwMFJOyt") & mkset("EtRYlumkyHDUTz:Ve}i\-nBJdcOqKZpWXNFbxShfs") & mkset("^IxRqKplz:fYoerTn uCMDiJVyNUAQE") & mkset("^z{AqXkswgMfaJdOIN:PjytRebU"))

print out
```

which gives us the flag,

    hitcon{Re:Zero -Starting Programming in Another World-}
