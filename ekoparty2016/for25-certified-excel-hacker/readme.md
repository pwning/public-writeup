## Certified Excel Hacker - Forensics 25 Problem

### Description

Can you wait for the answer?

### Overview

The given file, CALCULATOR.xlsm, appears to have a single worksheet named FORM that runs VBA script when the CALCULATE button 
is pressed. One can go through the trouble of unlocking the VBA and reversing the code, but it's a red herring. The actual 
answer is in a locked and hidden worksheet named ANSWER, where the flag is written out by coloring the cells.

### Correct Method

If you happen to look at Excel spreadsheet info for CALCULATOR.xlsm, you may notice that there are two spreadsheets - FORM 
and ANSWER - which are both protected. ANSWER doesn't appear in the workbook to begin with, so it's also hidden.

We can unprotect the worksheets in CALCULATOR.xlsm with any unprotect tool (I used https://excel.xartifex.com/). In 
Microsoft Excel, you can then open up the unprotected CALCULATOR.xlsm, go to Format > Hide & Unhide > Unhide Sheet... 
and unhide the ANSWER worksheet. The letters for the flag are made up of cells with black backgrounds.

**EKO{HIDDEN_SHEET_123}**

### The Other Rabbit Hole

If you're interested in what happens with the red herring of the VBA script on the FORM worksheet, you can read the following.

FORM's VBA code is also protected. You can easily unprotect it with the following method: 
http://stackoverflow.com/questions/1026483/is-there-a-way-to-crack-the-password-on-an-excel-vba-project. We then get the 
following VBA code:

```vba
Sub CALCULATE()
		Dim z57fbbe9a55b7e76e8772bb12c27d0537, NOT_ANSWER
		
		NOT_ANSWER = "NOTNOTNOTNOTNOTNOTNOTNOTNOTNOTNOTNOT"
		
		For z57fbbe9a55b7e76e8772bb12c27d0537 = 1 To 16777216
			answer = bfd9aaddb34d3018d0842fe01cd876ce2(answer)
		Next z57fbbe9a55b7e76e8772bb12c27d0537
		
		Hoja1.NOT_ANSWER.Text = "EKO{" + Replace(answer, "=", "") + "}"
	End Sub
	
	
	Public Function bfd9aaddb34d3018d0842fe01cd876ce2(ByVal sTextToHash As String)
		Dim b5d3ce0d93bdc39075041314952e56a03 As Object, be07792f9d366fe5e26844e720f7fd830 As Object
		Dim TextToHash() As Byte
		
		Set b5d3ce0d93bdc39075041314952e56a03 = CreateObject("System.Text.UTF8Encoding")
		Set be07792f9d366fe5e26844e720f7fd830 = CreateObject("System.Security.Cryptography.SHA1CryptoServiceProvider")
		
		TextToHash = b5d3ce0d93bdc39075041314952e56a03.Getbytes_4(sTextToHash)
		
		Dim bytes() As Byte
		
		bytes = be07792f9d366fe5e26844e720f7fd830.ComputeHash_2((TextToHash))
		
		bfd9aaddb34d3018d0842fe01cd876ce2 = bbdc49a038db5a02827fb9a3373d77989(bytes)
		
		Set b5d3ce0d93bdc39075041314952e56a03 = Nothing
		Set be07792f9d366fe5e26844e720f7fd830 = Nothing
	End Function
	
	
	Private Function bbdc49a038db5a02827fb9a3373d77989(ByRef arrData() As Byte) As String
		Dim bc5197ca332c6a81c0e410b8010ffd7c1
		Dim bde1a23ed20269f4573007d67e676a5e1
		
		Set bc5197ca332c6a81c0e410b8010ffd7c1 = CreateObject("MSXML2.DOMDocument")
		Set bde1a23ed20269f4573007d67e676a5e1 = bc5197ca332c6a81c0e410b8010ffd7c1.createElement("b64")
		
		bde1a23ed20269f4573007d67e676a5e1.DataType = "bin.base64"
		bde1a23ed20269f4573007d67e676a5e1.nodeTypedValue = arrData
		bbdc49a038db5a02827fb9a3373d77989 = bde1a23ed20269f4573007d67e676a5e1.Text
		
		Set bde1a23ed20269f4573007d67e676a5e1 = Nothing
		Set bc5197ca332c6a81c0e410b8010ffd7c1 = Nothing
	End Function
```

So quickly looking over this, it looks like we repetitively (16777216 times) take answer, and set the answer to the 
base 64-encoded SHA1 hash of answer. The false_solve.py script solves this. The result was 
EKO{DCEUslnl7DeiLWSdCLi0l1fxdc8}, but it was just a false lead.
