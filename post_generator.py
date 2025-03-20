from llm_assistant import llm
from prepare_dataframe import DataFrameBuilder
# Initialize DataFrameBuilder instance
chats = DataFrameBuilder()


def get_text_length(length):
    """Returns the approximate number of lines based on the selected length."""
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "5 to 10 lines"
    elif length == "Long":
        return "11 to 15 lines"


def get_prompt(length, language, tag):
    """Generates a prompt for the LLM to create a LinkedIn post."""
    text_length = get_text_length(length)
    prompt = f''' Generate a LinkedIn post using the below information. No preamble.
        1. Topic: {tag}
        2. Length: {text_length}
        3. language: {language}
        If language is Hinglish then it means it is a mix of Hindi and English.
        The script of the generated post should be English.
        '''
    # Fetch past posts matching the criteria
    chat_history = chats.get_filtered_posts(length, language, tag)

    # If relevant past posts exist, include them as examples for writing style
    if len(chat_history) > 0:
        prompt += " 4. Use the writing style as per the following examples."
        for i, post in enumerate(chat_history):
            post_text = post["text"]
            prompt += f"\n Example {i + 1}: \n {post_text}"
            if i == 1:  # Limit to two examples
                break
    return prompt


def generate_post(length, language, topic):
    """Uses LLM to generate a LinkedIn post based on the provided parameters."""
    prompt = get_prompt(length, language, topic)
    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    # Fetch and print filtered posts for debugging
    posts = chats.get_filtered_posts("Medium", "English", "Job Search")
    print(posts)
