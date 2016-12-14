






















def pad(instr, length):
	return instr + ' ' * (length - (len(instr) % length )) #25 -- data is nonzero dict

def encrypt_block(key, plaintext):
	encobj = AES.new(key, AES.MODE_ECB) #28 -- key must be correct len
	return encobj.encrypt(plaintext).encode('hex') #29 -- key length is 24 or 32












def xor_blocks(first,second):

	for i in range:
		first[i] = chr(ord(first[i]) ^ ord(second[i]))









def encrypt_cbc(key, IV, plaintext):
	if(len(plaintext) % len(key) != 0): #56 -- plaintext or key is an int
		plaintext = pad(plaintext, len(key)) #57 -- data is nonzero dict
	blocks = [plaintext[x:x+len(key)] for x in range(0,len(plaintext),len(key))] #58 -- data is dict of len key
	for i in range(len(blocks)):
		if i == 0:
			ctxt = xor_block(blocks[i], IV) #61 -- data is array of same length as key
			ctxt = encrypt_block(key,ctxt) #62 -- key must be correct len
		else:
			tmp = xor_block(blocks[i],ctxt[-1 * (len(key) * 2):].decode('hex')) #len(key) * 2 because ctxt is an ASCII string that we convert to "raw" binary. #64 array of len key chars + array of len key ints
			ctxt += tmp

	return ctxt #67




























def encrypt_data(encData):
	enc = encrypt_cbc(self.key, self.iv, encData['data']) #97 -- key must be correct len
















def dataReceived():
	self.key = encData['key'] #115 -- no key

	op = encData['op'] = #117 -- no op
	self.ops[op](encData) # just enc 4 now #118 -- op is wrong





