import string
import random
from django.core.cache import cache 


def send_otp(phone, code):
    print("=================OTP_SEND====================")
    print(f"Phone {phone} | Code : {code}")


class OTP:
    
    @staticmethod
    def generate_code():
        digits = string.digits
        return "".join(random.choice(digits) for _ in range(6))

    @staticmethod
    def send_otp_for_user(user_phone):
        code = OTP.generate_code()
        otp = cache.set(f"otp_{user_phone}", code, timeout=120)
        print(f"======================= Otp Code : {code} | Expires in 2 minutes!!! =======================")
        send_otp(user_phone, code)
        return code

    @staticmethod
    def verify_otp(user_phone, otp_code):
        otp = cache.get(f"otp_{user_phone}")
        if otp and otp_code == otp:
            print("Code Verified")
            cache.delete(otp)
            return True
        else:
            print("Code Invalid!!")
            return False
        
    @staticmethod
    def resend_otp(user_phone):
        otp = cache.get(f"otp_{user_phone}")
        if otp:
            cache.delete(otp)
        OTP.send_otp_for_user(user_phone)
        return "Code Send"





