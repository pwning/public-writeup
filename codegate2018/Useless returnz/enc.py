#-*- coding: utf-8 -*-

class Encrypt():

    def __init__(self, iv=None, keystr=None):        
        self.iv = "useles5@"
        self.keystr = "SUCK_7h15+4lG0_!"
        self.init_matrix = []

        chunk1 = self.keystr[0:8]
        chunk2 = self.keystr[8:16]
        row = []


        for i in range(0, 8):
            for j in range(0, 8):
                row.append(ord(chunk1[i]) ^ ord(chunk2[j]))
            
            self.init_matrix.append( row[0:8])
            
            del row[:]


    
    def split(self, p_txt):

        chunk = []

        if len(p_txt)%8 != 0:
            p_txt += "x" * (8 - len(p_txt)%8)
        

        for i in range(0, len(p_txt), 8 ):
             chunk.append(p_txt[i:i+8])
        

        return chunk

    
    def change(self, p_txt):
        
        temp = []
        result = []

        p_chunk = self.split(p_txt)

        for i in range(0, len(p_chunk)):
            for j in range(0, 8):
                temp.append(ord(p_chunk[i][j]))
            
            result.append(temp[0:8])
            del temp[:]
        

        return result


    def schedule(self, num):

        shift = [1, 2, 3, 2, 2, 1, 2, 3]
        temp = []
        matrix = []
        

        if num%2 == 0:            
            for i in range(0, 8):
                for j in range(0, 8):
                    temp.append(self.init_matrix[i][(8 - shift[i] + j)%8])
                    
                matrix.append(temp[0:8])
                del temp[:]
                
        
        else:
            for i in range(0, 8):
                for j in range(0, 8):
                    temp.append(self.init_matrix[i][(shift[i] + j)%8])

                matrix.append(temp[0:8])
                del temp[:]

            
        return matrix



    def round0(self, p_chunk, k_chunk):

        temp = []

        temp.append(p_chunk[0] - 10 + k_chunk[0])
        temp.append(p_chunk[1] ^ k_chunk[1])            
        temp.append(p_chunk[2] + k_chunk[2])
        temp.append(p_chunk[3] % (k_chunk[3]+2) + 32)
        temp.append(p_chunk[4] * 2 - k_chunk[3] - 7)
        temp.append(p_chunk[5] - 11 - k_chunk[5]%13)
        temp.append(p_chunk[6] ^ k_chunk[6])            
        temp.append(p_chunk[7] * 5 / (k_chunk[7] + 5))

        return temp
    


    def round1(self, p_chunk, k_chunk):

        temp = []

        temp.append(p_chunk[0] - 11 + k_chunk[0])
        temp.append(p_chunk[1] ^ (k_chunk[1])%5)
        temp.append(p_chunk[2] ^ k_chunk[2])            
        temp.append(p_chunk[3] % (k_chunk[3]+2) + 34)
        temp.append(p_chunk[4] - k_chunk[3] + 14)
        temp.append(p_chunk[5] ^ k_chunk[5])           
        temp.append(p_chunk[6] + 9 - k_chunk[6])
        temp.append(p_chunk[7] + k_chunk[7])

        return temp
    


    def round2(self, p_chunk, k_chunk):
        
        temp = []

        temp.append(p_chunk[0] - 11 + k_chunk[0])
        temp.append(p_chunk[1] ^ (k_chunk[1]) % 13)
        temp.append(p_chunk[2] + k_chunk[2] + 17)
        temp.append(p_chunk[3] ^ k_chunk[3])            
        temp.append(p_chunk[4] ^ k_chunk[4])            
        temp.append(p_chunk[5] - k_chunk[5] + 20)
        temp.append(p_chunk[6] / 3 % (k_chunk[6]+15))
        temp.append(p_chunk[7] + k_chunk[7])
        
        return temp



    def round3(self, p_chunk, k_chunk):
        
        temp = []

        temp.append(p_chunk[0] + k_chunk[0])
        temp.append(p_chunk[1] ^ k_chunk[1] - 15)
        temp.append(p_chunk[2] ^ k_chunk[2])            
        temp.append(p_chunk[3] + k_chunk[3])            
        temp.append(p_chunk[4] + k_chunk[3] - 33)
        temp.append(p_chunk[5] ^ k_chunk[5])            
        temp.append(p_chunk[6] + k_chunk[6] - 55)
        temp.append(p_chunk[7] + k_chunk[7])
        
        return temp



    def round4(self, p_chunk, k_chunk):
        
        temp = []

        temp.append(p_chunk[0] + k_chunk[0])
        temp.append(p_chunk[1] + k_chunk[1] + 17)
        temp.append(p_chunk[2] ^ k_chunk[2])            
        temp.append(p_chunk[3] - k_chunk[3] + 20)            
        temp.append(p_chunk[4] % (k_chunk[3]+2) - 34)
        temp.append(p_chunk[5] ^ k_chunk[5])            
        temp.append(p_chunk[6] + k_chunk[6])
        temp.append(p_chunk[7] - 11 + k_chunk[7])

        return temp


    def round5(self, p_chunk, k_chunk):
        
        temp = []

        temp.append(p_chunk[0] / 6 % (k_chunk[0]+1))
        temp.append(p_chunk[1] ^ k_chunk[1])            
        temp.append(p_chunk[2] - k_chunk[2] + 20)            
        temp.append(p_chunk[3] - k_chunk[3] + 20)            
        temp.append(p_chunk[4] % (k_chunk[3]+7) - 34)
        temp.append(p_chunk[5] + k_chunk[5])
        temp.append(p_chunk[6] ^ k_chunk[6])            
        temp.append(p_chunk[7] + k_chunk[7])      

        return temp


    def round6(self, p_chunk, k_chunk):
        
        temp = []

        temp.append(p_chunk[0] / 6 % (k_chunk[0]+7))
        temp.append(p_chunk[1] + k_chunk[1])
        temp.append(p_chunk[2] ^ k_chunk[2])            
        temp.append(p_chunk[3] - k_chunk[3] % 2 + 55)            
        temp.append(p_chunk[4] % (k_chunk[3]+3) + 127)
        temp.append(p_chunk[5] ^ k_chunk[5])            
        temp.append(p_chunk[6] + k_chunk[6] % 3)
        temp.append(p_chunk[7] + 11 + k_chunk[7])       

        return temp


    def round7(self, p_chunk, k_chunk):
        
        temp = []

        temp.append(p_chunk[0] + k_chunk[0]%30)
        temp.append(p_chunk[1] / (k_chunk[1]+1))
        temp.append(p_chunk[2] % (k_chunk[2]+4) + 18)            
        temp.append(p_chunk[3] ^ k_chunk[3])            
        temp.append(p_chunk[4] ^ k_chunk[4])            
        temp.append(p_chunk[5] / (k_chunk[5]+10) + 97)
        temp.append(p_chunk[6] + k_chunk[6])            
        temp.append(p_chunk[7] / 11 + k_chunk[7])       

        return temp
    


    def xor_calc(self, iv, chunk):
        
        result = []

        for i in range(0, 8):
            result.append(iv[i] ^ chunk[i])

        return result



    def encblock(self, chunk, num):

        rows = self.schedule(num)

        block = []
        result = []

        block.append(self.round0(chunk, rows[0]))
        block.append(self.round1(chunk, rows[1]))
        block.append(self.round2(chunk, rows[2]))
        block.append(self.round3(chunk, rows[3]))
        block.append(self.round4(chunk, rows[4]))
        block.append(self.round5(chunk, rows[5]))
        block.append(self.round6(chunk, rows[6]))
        block.append(self.round7(chunk, rows[7]))


        if num%2 == 0:
            result.append(chunk[0]^block[0][1]^block[1][2]^block[2][3])
            result.append(chunk[1]^block[0][1]^block[1][2]^block[3][2])
            result.append(chunk[2]^block[0][1]^block[2][3]^block[3][2])
            result.append(chunk[3]^block[1][2]^block[2][3]^block[3][2])
            result.append(chunk[4]^block[4][2]^block[5][1]^block[6][2])
            result.append(chunk[5]^block[4][2]^block[5][1]^block[7][3])
            result.append(chunk[6]^block[4][2]^block[6][2]^block[7][3])
            result.append(chunk[7]^block[5][1]^block[6][2]^block[7][3])

        else:
            result.append(chunk[0]^block[0][6]^block[1][5]^block[2][4])
            result.append(chunk[1]^block[0][6]^block[1][5]^block[3][5])
            result.append(chunk[2]^block[0][6]^block[2][4]^block[3][5])
            result.append(chunk[3]^block[1][5]^block[2][4]^block[3][5])
            result.append(chunk[4]^block[4][5]^block[5][6]^block[6][5])
            result.append(chunk[5]^block[4][5]^block[5][6]^block[7][4])
            result.append(chunk[6]^block[4][5]^block[6][5]^block[7][4])
            result.append(chunk[7]^block[5][6]^block[6][5]^block[7][4])
            

        return result



    def encrypt(self, plaintxt):

        p_chunks = self.change(plaintxt)
        e_chunks = []

        for i in range(0, len(p_chunks)):
            if i == 0:
                xor = (self.change(self.iv)[0])

            temp = self.xor_calc(xor, p_chunks[i])
            e_chunks.append(self.encblock(temp, i))

            del xor[:]
            del temp[:]

            xor.extend(e_chunks[i])  
        

        enctxt = ""

        for i in range(0, len(e_chunks)):
            for j in range(0, 8):
                enctxt += chr(e_chunks[i][j])


        return enctxt.encode('hex')

e = Encrypt()
print e.encrypt('admin127.0.0.1')
