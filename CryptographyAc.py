import os
import hashlib

class CryptographyAc(object):
    
    def __init__(self,key,block=640000):
        if type(key) == bytes:
            self.key = self.rand_the_key(key)
            self.path = self.temp(os.environ['AppData']+os.sep+'CryptographyAc')
            self.ePath = self.path+os.sep+'Encrypt.key'
            self.dPath = self.path+os.sep+'Decrypt.key'
            self.block = block
        else:
            raise TypeError ('Key must to be bytes')
    
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

    def spliter(self,data):
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

    def decrypt_first_key(self,val,key):
        t = self.xor(val,self.rand_the_key(key))
        k = self.rand_first_key(t,key)[0:1]
        key = self.rand_the_key(key + k)
        return key

    def encrypt(self,data):
        if type(data)!=bytes:
            raise TypeError ('Data must to be bytes')
        key = self.key
        f = open(self.ePath,'wb') 
        first = self.rand_first_key(bytes([data[0]]),key)
        f.write(self.xor(first,self.rand_the_key(key)))
        key = self.rand_the_key(key+bytes([data[0]]))
        for i in range(len(data)//self.block+1):
            for n in self.spliter(data[self.block*i:self.block*i+self.block]):
                f.write(self.xor(n,key))
                key = self.rand_the_key(key)
        f.close()
        return [open(self.ePath,'rb').read(), open(self.ePath,'wb').write(b'0')][0]


    def decrypt(self,data):
        if type(data)!=bytes:
            raise TypeError ('Data must to be bytes')
        with open(self.dPath,'wb')as d:
            key = self.decrypt_first_key(data[:64],self.key)
            data = data[64:]
            for i in range(len(data)//self.block+1):
                    for n in self.spliter(data[self.block*i:self.block*i+self.block]):
                        d.write(self.xor(n,key))
                        key = self.rand_the_key(key)
            d.close()
            return [open(self.dPath,'rb').read(), open(self.dPath,'wb').write(b'0')][0]
        
        
    def __permmited__(self,path):
        try:
            f=open(path,'rb').read1(1)
            f.close()
            f=open(path,'ab').write(b'')
            f.close()
            return True
        except:
            return False
            
        
    def encrypt_file(self,path):
        if self.__permmited__(path):
            with open(path, 'rb') as clear:
                with open(path,'wb') as cipher:
                    cipher.write(self.encrypt(eclear.read()))
            return True
        return 'Access is denied'
        
    def decrypt_file(self,path):
        if self.__permmited__(path):
            cipher=open(path,'rb')
            clear=open(path,'wb')
            clear.write(self.decrypt(cipher.read()))
            return True
        return 'Access is denied'
    
       
        
