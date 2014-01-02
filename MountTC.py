'''
Created on 15.12.2013

@author: lony
'''

import itertools, sys, time, multiprocessing
from subprocess import call
from multiprocessing.dummy import Pool  # use threads

word_list = [
"foo",
"bar",
"zoo",
"hello",
"World",
]
tc_file = r"C:\dev\tc-brute-force\test.pa"
tc_prog = r"C:\Program Files\TrueCrypt\TrueCrypt.exe"
tc_mount_letter = "z"
verbose = 1
number_of_workers = multiprocessing.cpu_count() * 10
curent_time = time.time()

def CRC32(data):
    """Compute CRC-32."""
    crc = binascii.crc32(data)
    # Convert from signed to unsigned word32.
    return crc % 0x100000000

def BE32(x):
    return struct.unpack(">L", x)[0]

class CipherChain:
    def __init__(self, ciphers):
        self.ciphers = [ciph() for ciph in ciphers]
    def set_key(self, keys):
        i = 0
        for cipher in self.ciphers:
            cipher.set_key(keys[i])
            i += 1
    def encrypt(self, data):
        for cipher in self.ciphers:
            data = cipher.encrypt(data)
        return data
    def decrypt(self, data):
        for cipher in reversed(self.ciphers):
            data = cipher.decrypt(data)
        return data
    def get_name(self):
        return '-'.join(reversed([cipher.get_name() for cipher in self.ciphers]))

Cascades = [
    [Rijndael],
    [Serpent],
    [Twofish],
    [Twofish, Rijndael],
    [Serpent, Twofish, Rijndael],
    [Rijndael, Serpent],
    [Rijndael, Twofish, Serpent],
    [Serpent, Twofish]
]

HMACs = [
    (HMAC_SHA1, "SHA-1"),
    (HMAC_RIPEMD160, "RIPEMD-160"),
    (HMAC_WHIRLPOOL, "Whirlpool")
]

def TCIsValidVolumeHeader(header):
    magic = header[0:4]
    checksum = BE32(header[8:12])
    return magic == 'TRUE' and CRC32(header[192:448]) == checksum

def TrueCryptVolume(password):
	fileobj = file(tc_file, "rb")
	salt = fileobj.read(64)
	header = fileobj.read(448)
	
	for hmac, hmac_name in HMACs:
            # Generate the keys needed to decrypt the volume header.
            iterations = 2000
            if hmac == HMAC_WHIRLPOOL:
                iterations = 1000

            info = ''
            if hmac_name in "RIPEMD-160 Whirlpool":
                info = ' (this will take a while)'
            progresscallback("Trying " + hmac_name + info)
            
            header_keypool = PBKDF2(hmac, password, salt, iterations, 128)
            header_lrwkey = header_keypool[0:16]
            header_key1 = header_keypool[32:64]
            header_key2 = header_keypool[64:96]
            header_key3 = header_keypool[96:128]

            for cascade in Cascades:
                # Try each cipher and cascades and see if we can successfully
                # decrypt the header with it.
                cipher = CipherChain(cascade)
                
                progresscallback("..." + cipher.get_name())
                
                cipher.set_key([header_key1, header_key2, header_key3])
                decrypted_header = LRWMany(cipher.decrypt, header_lrwkey, 1, header)
                if TCIsValidVolumeHeader(decrypted_header):
                    # Success.
                    return
        # Failed attempt.
        raise KeyError, "incorrect password (or not a truecrypt volume)"

if __name__ == '__main__':
		TrueCryptVolume("helloWorld")
