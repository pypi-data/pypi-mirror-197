from dependencies import *

@st.experimental_memo
def generate_otp():
    digits = "0123456789"
    otp = ""
    for i in range(4):
        otp += digits[random.randint(0, 9)]
    return otp