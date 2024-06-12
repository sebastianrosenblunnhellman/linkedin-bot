import streamlit as st
from Router.Recommender import Recommender

def run_recommender(email, password):
    bot = Recommender()
    bot.login(email, password)
    bot.recommend()

def main():
    st.title("LinkedIn Recommender Bot")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Run Recommender"):
        if email and password:
            st.write("Running the recommender bot...")
            run_recommender(email, password)
            st.write("Recommender bot has finished running.")
        else:
            st.write("Please enter both email and password.")

if __name__ == "__main__":
    main()
