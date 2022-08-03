import os
import hashlib

class CryptoAc(object):
    
    def __init__(self,key):
        self.key=rand_the_key(key)
        self.path=self.temp(os.environ['AppData']+os.sep+'CryptographyAc')
        self.ePath=self.path+os.sep+'Encrypt.key'
        self.dPath=self.path+os.sep+'Decrypt.key'
    
    
    def temp(self,path):
        try:
            os.mkdir(path)
        except:
            pass
        return path


    def xor(self,a,b):
        return bytes(i^j for i, j in zip(a, b))

    def rand_the_key(self,key):
        return hashlib.sha512(key).digest()

    def spliter(self,data,key):
        splited=[]
        for i in range(0,len(data),64):
            splited.append(data[i:i+64])
        return splited


    def rand_first_key(self,val,key):
        l=len(val)
        g=l
        c=0
        while l<64+g:
            val+=bytes([val[c]^key[c]])
            l+=1
            c+=1
        return val[g:]


    def decrypt_first_key(self,val):
        t = xor(val,rand_the_key(self.key))
        k = rand_first_key(t,self.key)[0:1]
        key = rand_the_key(self.key + k)
        return key


    def encrypt(self,data):
        key = self.key
        f = open(self.ePath,'wb') 
        first = rand_first_key(bytes([data[0]]),key)
        f.write(xor(first,rand_the_key(key)))
        key = rand_the_key(key+bytes([data[0]]))
        print(key)
        for i in range(len(data)//640000+1):
            for n in spliter(data[640000*i:640000*i+640000]):
                f.write(xor(n,key))
                key = rand_the_key(key)
        f.close()
        return [open(self.ePath,'rb').read(), open(self.ePath,'wb').write(b'0')][0]


    def decrypt(self,data):
        with open('Decryptionpro.txt','wb')as d:
            key = decrypt_key(data[:64],self.key)
            print(key)
            data = data[64:]
            for i in range(len(data)//640000+1):
                    for n in spliter(data[640000*i:640000*i+640000]):
                        d.write(xor(n,key))
                        key = rand_the_key(key)
            d.close()
            return [open('Decryptionpro.txt','rb').read(), open('Decryptionpro.txt','wb').write(b'0')][0]
          
          
          
        
