import pyotp
import qrcode

# it is important. Length 32
# pyotp.random_base32() -> WUPEY3MK7JOHWQRMRPGEETIQOWKB7Y6O
key = "KrolegTestIsBestForEverythingBro"

uri = pyotp.totp.TOTP(key).provisioning_uri(
    name='Kr_Oleg',
    issuer_name='KrolegTest')

print(uri)

# Qr code generation step. Uncomment for first run.
# qrcode.make(uri).save("qr.png")

totp = pyotp.TOTP(key)

# verifying the code
while True:
    print(totp.verify(input("Enter the Code : ")))


