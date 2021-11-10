from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from hashlib import sha256


class generateKey(object):
    def __init__(self, init_key):
        self.init_key = init_key

    def do_encode(self):
        sha256_key = sha256(self.init_key.encode('utf-8')).hexdigest()
        # print(sha256_key)
        return sha256_key


class generateAesKey(object):
    def __init__(self, encode_key, sha256_key):
        self.encode_key = encode_key
        self.sha256_key = sha256_key
        self.mode = AES.MODE_CBC

    def deal_text(self):
        if len(self.encode_key.encode('utf-8')) % 16:
            n = 16 - len(self.encode_key.encode('utf-8')) % 16
            return (self.encode_key + (n * '\0')).encode('utf-8')

    def do_encode(self):
        key = self.sha256_key[:16].encode('utf-8')
        vi = self.sha256_key[48:].encode('utf-8')
        cryptos = AES.new(key, self.mode, vi)
        text = cryptos.encrypt(self.deal_text())
        print('加密后的密码为{0}'.format(b2a_hex(text)))
        return b2a_hex(text)

    def do_decode(self):
        key = self.sha256_key[:16].encode('utf-8')
        vi = self.sha256_key[48:].encode('utf-8')
        cryptos = AES.new(key, self.mode, vi)
        text = cryptos.decrypt(a2b_hex(self.encode_key))
        print('解密后的密码为{0}'.format(bytes.decode(text).rstrip('\0')))
        return bytes.decode(text).rstrip('\0')


if __name__ == '__main__':
    print('需要加密还是解密？')
    judge_nu = input("加密输入0，解密输入1---------------\n:")
    if judge_nu == '0' or 0:
        init_key = input('请输入密钥----------------\n:')
        encode_key = input('请输入需要加密的密码,不超过16位---------------\n:')
        generate_key = generateKey(init_key)
        sha256_key = generate_key.do_encode()
        generate_aesKey = generateAesKey(encode_key, sha256_key)
        generate_aesKey.do_encode()

    elif judge_nu == '1' or 1:
        init_key = input('请输入密钥------------------\n:')
        decode_key = input('请输入需要解密的密码----------------\n:')
        generate_key = generateKey(init_key)
        sha256_key = generate_key.do_encode()
        generate_aesKey = generateAesKey(decode_key, sha256_key)
        generate_aesKey.do_decode()

    else:
        print('请输入合法值-----------------------')
        exit(0)
