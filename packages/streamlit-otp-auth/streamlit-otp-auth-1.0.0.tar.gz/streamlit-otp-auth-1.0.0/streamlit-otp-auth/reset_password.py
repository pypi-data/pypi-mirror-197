from dependencies import *
from generate_otp import *
from send_otp import *

if "load_state" not in st.session_state:
    st.session_state.load_state = False

def reset_password():
    if st.button("Forgot password") or st.session_state.load_state:
        st.session_state.load_state = True
        email = str(st.text_input("Email"))
        otp_password = st.text_input("Enter your Otp set to email")
        reset_otp = generate_otp()
        if st.button("Send OTP") :
            send_otp_to_email(email, reset_otp)
            st.write("Your password reset otp has benn sent to your registered email address")
        if otp_password == reset_otp:
            new_password = st.text_input("Enter your new password : ")
            new_password_confirm = st.text_input("Confirm your new password : ")
            if st.button("Reset password") :
                users = {}
                try:
                    with open("users.yaml",'r') as file :
                        users = yaml.load(file,Loader = yaml.FullLoader)
                except:
                    pass
                if new_password_confirm == new_password and email in users:
                    st.experimental_memo.clear()
                    users[email]["password"] = new_password
                    with open("users.yaml", "w") as file:
                        yaml.dump(users, file)
                    st.success("Password Reset Suucessful")
                elif new_password != new_password_confirm:
                    st.error("Passwords do not match")
                else:
                    st.error("User registration not found. Please check your entered address or signup")
            elif otp_password != reset_otp:
                st.write("Please enter correct OTP")