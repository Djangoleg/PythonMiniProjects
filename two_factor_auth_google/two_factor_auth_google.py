import pyotp
import qrcode

# it is important. Length 32
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




