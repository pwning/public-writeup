" note: split lines by inserting "\nexe "norm! 

fun! LoadBlock1 ()
" Arguments: `Z
" Save: `b, `c
" Stack range: XYZ
exe "norm! `bmY`cmX`Zmb"
exe "norm! Go\<esc>ma`amc"
exe "norm! `b:exe \"let g:l=getline('.')\"\<cr>`co\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[0:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[1:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[2:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[3:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[4:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[5:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[6:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[7:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[8:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[9:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[10:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[11:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[12:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[13:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[14:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[15:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! `cJ`cma"
exe "norm! `Xmc`Ymb"

endfun

fun! LoadBlock2()
" Arguments: `Z
" Save: `b, `c
" Stack range: XYZ
exe "norm! `bmY`cmX`Zmb"
exe "norm! Go\<esc>ma`amc"
exe "norm! `b:exe \"let g:l=getline('.')\"\<cr>`co\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[16:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[17:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[18:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[19:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[20:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[21:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[22:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[23:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[24:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[25:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[26:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[27:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[28:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[29:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[30:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! :exe \"norm! \".(strgetchar(g:l[31:], 0) % 32 + 1).\"ax\"\<cr>^rXo\<esc>"
exe "norm! `cJ`cma"
exe "norm! `Xmc`Ymb"

endfun

fun! Multiply ()
" Arguments: `L, `K
" Return: `a (copied to `dP)
" Save: `b, `c, `d, `e
" Stack range: GHIJKL

" Store arguments and saved registers
exe "norm! `bmJ`cmI`dmH`emG`Kmb`Lmc"
" New working space: d = a = working area
exe "norm! Go\<esc>ma`amd"
" copy b to d, insert X on next line
exe "norm! `byy`dP`dOX\<esc>"
" set e to the single X, d to the start of the block, remove leading X from d
exe "norm! me`d{jmd`dx"

" 32 iterations of addition (add `c to `e, and decrement `d)
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `cyy`eP`dvyjPxxVy`epkJx`dxjV`ekd`ex:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"

" Join `d to the next line
exe "norm! `dJ`dma"
" Restore registers
exe "norm! `Gme`Hmd`Imc`Jmb"
endfun


fun! Multiply4 ()
" Arguments: `R, `Q
" Save: `b, `c, `d, `e
" Stack range: MNOPQR

" Store arguments and saved registers
exe "norm! `bmP`cmO`dmN`emM`Qmb`Rmc"
" New working space: d = a = working area
exe "norm! Go\<esc>ma`amd"

exe "norm! `bmL`cmK"
call Multiply()
exe "norm! `ame`eyy`dP`eV}dggme"

exe "norm! `b1jmb`c1jmc"
exe "norm! `bmL`cmK"
call Multiply()
exe "norm! `ame`eyy`dP`eV}dggme"

exe "norm! `b1jmb`c1jmc"
exe "norm! `bmL`cmK"
call Multiply()
exe "norm! `ame`eyy`dP`eV}dggme"

exe "norm! `b1jmb`c1jmc"
exe "norm! `bmL`cmK"
call Multiply()
exe "norm! `ame`eyy`dP`eV}dggme"

" Set d to start of working space
exe "norm! `d{jmd"
" Join all four results together
exe "norm! `dJxxJxxJxx"
" mod 32
exe "norm! :s/\\(x\\{32}\\)*//g\<cr>"
" Store result in a
exe "norm! `dma"
" Restore registers
exe "norm! `Mme`Nmd`Omc`Pmb"
endfun

fun! Transpose()
" Arguments: `R
" Save: `b, `c, `d
" Stack range: OPQR
exe "norm! `bmQ`cmP`dmO`Rmb"
" Setup working area at `c
exe "norm! Go\<esc>ma`amc"

" Copy lines 0,4,8,12 to `c
exe "norm! `bmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
" Copy lines 1,5,9,13 to `c
exe "norm! `b1jmb`bmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
" Copy lines 2,6,10,14 to `c
exe "norm! `b1jmb`bmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
" Copy lines 3,7,11,15 to `c
exe "norm! `b1jmb`bmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
exe "norm! `d4jmd`dyy`cP"
" Set `a to start of block
exe "norm! `c{jmc`cma"
exe "norm! `Omd`Pmc`Qmb"
endfun

fun! Multiply4x4()
" Arguments: `Z, `Y
" Save: `b, `c, `d, `e, `f, `g
" Stack range: STUVWXYZ
exe "norm! `bmX`cmW`dmV`emU`fmT`gmS"
exe "norm! `Ymb`Zmc"
exe "norm! Go\<esc>ma`amd"

exe "norm! `cmR"
call Transpose()
exe "norm! `ame"

exe "norm! `emf"

" e[:4] * b[:4]
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

" e[4:8] * b[:4]
exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

" e[8:12] * b[:4]
exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

" e[12:16] * b[:4]
exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `b4jmb"
exe "norm! `emf"

exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `b4jmb`emf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `b4jmb`emf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `f4jmf"
exe "norm! `fmR`bmQ"
call Multiply4()
exe "norm! `amg`gyy`dP`gV}dggmg"

exe "norm! `eV}dggme`d{jmd`dma`Smg`Tmf`Ume`Vmd`Wmc`Xmb"
endfun

fun! Something4()
exe "norm! `bmH`cmG`dmF`Imb`JmcGo\<esc>"
exe "norm! ma`amd`byy`dP`cyy`dP`d{jmd`dJxx^x:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `dma`Fmd`Gmc`Hmb"
endfun

fun! Something()
exe "norm! `bmQ`cmP`dmO`emN`Rmb"

exe "norm! `bmM`bmL`cmK`Mmb"
exe "norm! Go\<esc>ma`amc"
exe "norm! `byy`cP"
exe "norm! `c{jmc"
exe "norm! `cxaxx\<esc>"
exe "norm! :s/^\\(\\%(xx\\)*\\)x\\?$/\\1/g\<cr>:s/xx/x/g\<cr>xaxx\<esc>"
exe "norm! :s/^\\(\\%(xx\\)*\\)x\\?$/\\1/g\<cr>:s/xx/x/g\<cr>xIX\<esc>"
exe "norm! `cma"
exe "norm! `Kmc`Lmb"

exe "norm! `amc"

exe "norm! `bmM`bmL`cmK`Mmb"

exe "norm! `bmJ`bmI"
call Something4()
exe "norm! `amb"

exe "norm! `bmJ`bmI"
call Something4()
exe "norm! `amc"

exe "norm! `bV}dggmb"
exe "norm! `cmb"

exe "norm! `bmJ`bmI"
call Something4()
exe "norm! `amc"

exe "norm! `bV}dggmb"
exe "norm! `cmb`bma"
exe "norm! `Kmc`Lmb"
exe "norm! `amd"

exe "norm! `dmM`cmL"

exe "norm! `bmK`cmJ`dmI`Lmb"
exe "norm! `MmcGo\<esc>ma`amd"
exe "norm! `byy`dP"
exe "norm! `cyy`dP"
exe "norm! `d{jmd"
exe "norm! `dJxx^x"
exe "norm! :s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `dma"
exe "norm! `Imd`Jmc`Kmb"

exe "norm! `ame"
exe "norm! `dV}dggmd"
exe "norm! `cV}dggmc"

exe "norm! `ema"
exe "norm! `Nme`Omd`Pmc`Qmb"
endfun

fun! Something2()
exe "norm! `bmP`cmO`dmN`Qmb`RmcGo\<esc>"
exe "norm! ma`amd`byy`dP`cyy`dP`d{jmd`dJxx^x:s/\\(x\\{32}\\)*//g\<cr>IX\<esc>"
exe "norm! `dma`Nmd`Omc`Pmb"
endfun

fun! MungeCore()
" b = B*B
" c = B*B*C
exe "norm! `d1kme"

exe "norm! `bmR"
call Something()
exe "norm! `amf"

exe "norm! `cmR"
call Something()
exe "norm! `amg"

exe "norm! `emR`fmQ"
call Something2()
exe "norm! `ame"

exe "norm! `fV}dggmf"

exe "norm! `emR`gmQ"
call Something2()
exe "norm! `amf"

exe "norm! `eV}dggme"
exe "norm! `gV}dggmg"
exe "norm! `fyy`dP"
exe "norm! `fV}dggmf"
exe "norm! `b1jmb"
exe "norm! `c1jmc"
endfun

fun! Munge()
exe "norm! `bmX`cmW`dmV`emU`fmT`gmS`Ymb`Zmc"
exe "norm! Go\<esc>ma`amd"
" Put an X at `d
exe "norm! `dOX\<esc>"
" Munge 16x
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
call MungeCore()
" Kill first char of `d and join
exe "norm! `d{jmdxJ"
exe "norm! `dma"
exe "norm! `Smg`Tmf`Ume`Vmd`Wmc`Xmb"
endfun

fun! DuplicateBlock()
" Arguments: `W
exe "norm! `bmV`Wmb"
" Copy block `b to `a at the end of the file.
exe "norm! `bV}yGpma"
exe "norm! `Vmb"
endfun

fun! CheckSolution()
exe "norm! `bmY`cmX`Zmb"

exe "norm! `bmW"
call DuplicateBlock()
exe "norm! `amc"

exe "norm! `c"
exe "norm! :s/X\\(x\\{23}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{30}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{17}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{21}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{26}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{7}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{22}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{3}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{1}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{18}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{4}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{17}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{2}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{10}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{21}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"
exe "norm! :s/X\\(x\\{9}\\)\\?/X/g\<cr>:s/X\\(x\\?\\)x*/X\\1/g\<cr>j"

" Join all lines together and take OR
exe "norm! `cJxxJxxJxxJxxJxxJxxJxxJxxJxxJxxJxxJxxJxxJxxJxx"
exe "norm! :s/X\\(x\\?\\)x*/X\\1/g\<cr>"
exe "norm! `Xmc`Ymb"
endfun

fun! Main ()

exe "norm! ggdGiWelcome to th1s flag checker written in vim script.\nEnter the flag in Balsn{.+} format and then press <Enter>.\n\nThis script is tested with vim 8.0.1453 + default vimrc (ubuntu 18.04).\nIf it runs very slow, try to disable X11 forwarding before launching vim.\nIt should terminate in 30 seconds.\n\n>\ Balsn{this_is_test_flag_r}\<esc>"
" Join first few lines
exe "norm! ggJxJxJxJxJxJx"
" Keep only first 16 chars
exe "norm! ^16ld$"
" Replace spaces to underscores
exe "norm! :s/ /_/g\<cr>"
" Join that ("Welcome_to_th1s_") to the input flag, minus trailing r
exe "norm! j:s/^> Balsn{\\([a-z_]\\+\\)r}$/\\1/g\<cr>"
exe "norm! :%s/\\n//g\<cr>"
" rot13 everything
exe "norm! ^v$g?O\<esc>"
" add preceding newline to make a block
exe "norm! jo\<esc>"
exe "norm! ggmambmcmdmemfmgmhmimjmkmlmmmnmompmqmrmsmtmumvmwmxmymz"

" b = &flag
exe "norm! ggjmb"

exe "norm! `bmZ"
call LoadBlock1()
exe "norm! `amc"

exe "norm! `bmZ"
call LoadBlock2()
exe "norm! `amd"

" Delete flag block
exe "norm! `bV}dggmb"
" b = &block1
" c = &block2
exe "norm! `cmb`dmc"

" Compute B * B
exe "norm! `bmZ`bmY"
call Multiply4x4()
exe "norm! `amd"

" Compute B * B * C
exe "norm! `cmZ`dmY"
call Multiply4x4()
exe "norm! `ame"

exe "norm! `emZ`dmY"
call Munge()
exe "norm! `amf"

exe "norm! `fmZ"
call CheckSolution()
exe "norm! `amg"

" Clear all function blocks
exe "norm! `bV}dggmb"
exe "norm! `cV}dggmc"
exe "norm! `dV}dggmd"
exe "norm! `eV}dggme"
exe "norm! `fV}dggmf"
" Clear the lines above and below the result
exe "norm! `gkddjdd"
" Check result == 0
exe "norm! :s/^X$/Correct/g\<cr>"

endfun

call Main()
