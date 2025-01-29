# Need to install cryptography package: pip install cryptography

import json
import base64
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Set to True if the JWK contains a private key that is encrypted and provides the password
encrypt_key = False
encryption_password = b'password'

pkcs_format = 'PKCS1'  # PKCS1 or PKCS8

# Helper: Base64URL decode
def base64url_decode(val: str) -> bytes:
    # Pad with '=' if needed
    val += '=' * ((4 - len(val) % 4) % 4)
    val = val.replace('-', '+').replace('_', '/')
    return base64.b64decode(val)

# Modify this to point to your JWK file
with open('myjwk.json', 'r') as f:
    jwk = json.load(f)

# JWK fields (string, base64url encoded)
n_b64 = jwk["n"]
d_b64 = jwk["d"]
p_b64 = jwk["p"]
q_b64 = jwk["q"]
dp_b64 = jwk["dp"]
dq_b64 = jwk["dq"]
qi_b64 = jwk["qi"]

# "e" might be included, but if not, the default is 65537
if "e" in jwk:
    e_b64 = jwk["e"]
    e = int.from_bytes(base64url_decode(e_b64), byteorder='big')
else:
    e = 65537  # typical RSA exponent if omitted

# Convert to big integers
n  = int.from_bytes(base64url_decode(n_b64),  byteorder='big')
d  = int.from_bytes(base64url_decode(d_b64),  byteorder='big')
p  = int.from_bytes(base64url_decode(p_b64),  byteorder='big')
q  = int.from_bytes(base64url_decode(q_b64),  byteorder='big')
dp = int.from_bytes(base64url_decode(dp_b64), byteorder='big')
dq = int.from_bytes(base64url_decode(dq_b64), byteorder='big')
qi = int.from_bytes(base64url_decode(qi_b64), byteorder='big')

# Reconstruct private key using RSA private numbers
private_key = rsa.RSAPrivateNumbers(
    p=p,
    q=q,
    d=d,
    dmp1=dp,
    dmq1=dq,
    iqmp=qi,
    public_numbers=rsa.RSAPublicNumbers(e, n)
).private_key()


# Determine serialization format
format_map = {
    'PKCS1': serialization.PrivateFormat.PKCS1,
    'PKCS8': serialization.PrivateFormat.PKCS8
}
private_format = format_map.get(pkcs_format, serialization.PrivateFormat.PKCS1)

# Determine encryption settings
encryption = serialization.BestAvailableEncryption(encryption_password) if encrypt_key else serialization.NoEncryption()

# Convert to PEM format
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=private_format,
    encryption_algorithm=encryption
)

# Print PEM contents
print(pem.decode())
