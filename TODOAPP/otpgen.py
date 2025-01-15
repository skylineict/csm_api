import pyotp





def otp_generator():
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.now()[:6] 