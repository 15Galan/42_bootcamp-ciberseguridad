import subprocess
import os

###
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
###

p0 = subprocess.run(["openssl", "prime", "-generate", "-bits", "256", "-hex"],
        stdout=subprocess.PIPE)
p0 = int(p0.stdout, 16)
p1 = subprocess.run(["openssl", "prime", "-generate", "-bits", "256", "-hex"],
        stdout=subprocess.PIPE)
p1 = int(p1.stdout, 16)
p2 = subprocess.run(["openssl", "prime", "-generate", "-bits", "256", "-hex"],
        stdout=subprocess.PIPE)
p2 = int(p2.stdout, 16)

n1 = p0 * p1
n2 = p0 * p2

e = 0x10001

r1 = (p0 - 1) * (p1 - 1)
r2 = (p0 - 1) * (p2 - 1)

d1 = modinv(e, r1)
d2 = modinv(e, r2)

e1_1 = d1 % (p0 - 1)
e1_2 = d1 % (p1 - 1)
e2_1 = d2 % (p0 - 1)
e2_2 = d2 % (p2 - 1)

coef1 = pow(p1, p0 - 2, p0)
coef2 = pow(p2, p0 - 2, p0)

with open("key1.conf", "w") as f:
    f.write("asn1=SEQUENCE:private_key\n[private_key]\nversion=INTEGER:0\n")
    f.write("n=INTEGER:" + hex(n1) + "\n")
    f.write("e=INTEGER:" + hex(e) + "\n")
    f.write("d=INTEGER:" + hex(d1) + "\n")
    f.write("p=INTEGER:" + hex(p0) + "\n")
    f.write("q=INTEGER:" + hex(p1) + "\n")
    f.write("exp1=INTEGER:" + hex(e1_1) + "\n")
    f.write("exp2=INTEGER:" + hex(e1_2) + "\n")
    f.write("coeff=INTEGER:" + hex(coef1) + "\n")

with open("key2.conf", "w") as f:
    f.write("asn1=SEQUENCE:private_key\n[private_key]\nversion=INTEGER:0\n")
    f.write("n=INTEGER:" + hex(n2) + "\n")
    f.write("e=INTEGER:" + hex(e) + "\n")
    f.write("d=INTEGER:" + hex(d2) + "\n")
    f.write("p=INTEGER:" + hex(p0) + "\n")
    f.write("q=INTEGER:" + hex(p2) + "\n")
    f.write("exp1=INTEGER:" + hex(e2_1) + "\n")
    f.write("exp2=INTEGER:" + hex(e2_2) + "\n")
    f.write("coeff=INTEGER:" + hex(coef2) + "\n")

os.system("openssl asn1parse -genconf key1.conf -out key1.der -noout")
os.system("openssl asn1parse -genconf key2.conf -out key2.der -noout")
os.system("openssl rsa -inform DER -outform PEM -in key1.der -out key1.pem")
os.system("openssl rsa -inform DER -outform PEM -in key2.der -out key2.pem")
os.system("openssl req -new -nodes -key key1.pem -out csr1.pem -subj /CN=ejemplo")
os.system("openssl req -new -nodes -key key2.pem -out csr2.pem -subj /CN=ejemplo")
os.system("openssl req -x509 -nodes -sha256 -days 36500 -key key1.pem -in csr1.pem -out cert1.pem")
os.system("openssl req -x509 -nodes -sha256 -days 36500 -key key2.pem -in csr2.pem -out cert2.pem")
os.system("rm -rf key1.conf key2.conf key1.der key2.der csr1.pem csr2.pem")

# Private keys
os.system("rm key1.pem key2.pem")

os.system("echo 'pwd42' > passwd.txt")
os.system("openssl x509 -pubkey -noout -in cert1.pem > pubkey.pem")
os.system("openssl rsautl -encrypt -inkey pubkey.pem -pubin -in passwd.txt -out passwd.enc")
os.system("echo 'You win!! This is the secret message.' > msg.txt")
os.system("openssl enc -in msg.txt -out encrypted_file.txt -e -aes256 -kfile passwd.txt")
os.system("rm pubkey.pem passwd.txt msg.txt")


# HOW TO
# Put the numbers into two text files in the appropriate format. Example:
'''
asn1=SEQUENCE:private_key
[private_key]
version=INTEGER:0

n=INTEGER:0xBB6FE79432CC6EA2D8F970675A5A87BFBE1AFF0BE63E879F2AFFB93644\
D4D2C6D000430DEC66ABF47829E74B8C5108623A1C0EE8BE217B3AD8D36D5EB4FCA1D9

e=INTEGER:0x010001

d=INTEGER:0x6F05EAD2F27FFAEC84BEC360C4B928FD5F3A9865D0FCAAD291E2A52F4A\
F810DC6373278C006A0ABBA27DC8C63BF97F7E666E27C5284D7D3B1FFFE16B7A87B51D

p=INTEGER:0xF3929B9435608F8A22C208D86795271D54EBDFB09DDEF539AB083DA912\
D4BD57

q=INTEGER:0xC50016F89DFF2561347ED1186A46E150E28BF2D0F539A1594BBD7FE467\
46EC4F

exp1=INTEGER:0x9E7D4326C924AFC1DEA40B45650134966D6F9DFA3A7F9D698CD4ABEA\
9C0A39B9

exp2=INTEGER:0xBA84003BB95355AFB7C50DF140C60513D0BA51D637272E355E397779\
E7B2458F

coeff=INTEGER:0x30B9E4F2AFA5AC679F920FC83F1F2DF1BAF1779CF989447FABC2F5\
628657053A
'''

# To construct the binary DER file:
# > openssl asn1parse -genconf <path to above file> -out newkey.der
# You can then run this through OpenSSL's rsa command to confirm:
# > openssl rsa -in newkey.der -inform der -text -check
# Convert DER Format To PEM Format For RSA Key
# > openssl rsa -inform DER -outform PEM -in mykey.der -out mykey.pem
# To get the public key from the private key
# > openssl rsa rsa -in mykey.pem -pubout > pubkey.pem

# https://stackoverflow.com/questions/19850283/how-to-generate-rsa-keys-using-specific-input-numbers-in-openssl
# https://stackoverflow.com/questions/33705487/how-to-calculate-the-coefficient-of-a-rsa-private-key

# ** To generate a certificate from the private key **
# Generate certificate request
# > openssl req -new -nodes -key mykey.pem -out csr.pem -subj /CN=ejemplo
# Generate self-signed certificate (sign the certificate request)
# > openssl req -x509 -nodes -sha256 -days 36500 -key mykey.pem -in csr.pem -out cert.pem
# Get public key from certificate
# > openssl x509 -pubkey -noout -in cert.pem > pubkey.pem

# ** Encrypt a message with a public key **
# > openssl rsautl -encrypt -inkey pubkey.pem -pubin -in top_secret.txt -out top_secret.enc
# Decrypt with the private key
# > openssl rsautl -decrypt -inkey mykey.pem -in top_secret.enc > top_secret.txt

# ** Encrypt/Decrypt with a symmetric key
# > openssl enc -in file.txt -out encrypted_file.txt -e -aes256
# # enter aes-256-cbc encryption password:
# > openssl enc -in encrypted_file.txt -out clear_text_file.txt -d -aes256
# # enter aes-256-cbc decryption password:
