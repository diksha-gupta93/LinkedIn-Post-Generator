import streamlit as st
from prepare_dataframe import DataFrameBuilder
from post_generator import generate_post

# Options for language and post length
language_options = ["Hinglish", "German", "English"]
length_options = ["Short", "Medium", "Long"]


def main():
    """Main function to render the LinkedIn Post Generator UI."""
    st.title("LinkedIn Post Generator")  # App title

    # Creating three columns for input selections
    col1, col2, col3 = st.columns(3)
    fs = DataFrameBuilder()  # Initializing the data frame builder

    # Dropdown for selecting post title (tag)
    with col1:
        selected_tag = st.selectbox("Title", options=fs.get_tags())

    # Dropdown for selecting post length
    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    # Dropdown for selecting language
    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    # Button to generate the LinkedIn post
    if st.button("Generate"):
        post = generate_post(selected_length, selected_language, selected_tag)  # Generate post
        st.write(post)  # Display the generated post


# Run the app when executed directly
if __name__ == "__main__":
    main()
