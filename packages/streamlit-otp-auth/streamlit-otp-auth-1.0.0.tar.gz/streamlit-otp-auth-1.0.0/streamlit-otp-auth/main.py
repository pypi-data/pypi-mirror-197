from dependencies import *
from signup import *
from login import *

if "load_state" not in st.session_state:
    st.session_state.load_state = False

def main():
    st.set_page_config(page_title="Authentication System", page_icon="🔒", layout="wide")
    st.title("Authentication System")
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                footer:after{
                    content:'        Copyright @ 2022: Anjishnu Saw (anjishnu@anjishnusaw.tk)';
                    display:bloack;
                    visibility: visible;
                    position:relative;
                    color:yellow
                }
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    menu = ["Sign Up", "Log In"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Sign Up":
        sign_up()
    elif choice == "Log In":
        log_in()


if __name__ == "__main__":
    main()
