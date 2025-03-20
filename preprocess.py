import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_assistant import llm
import re


def clean_text(text):
    """Removes non-ASCII characters from the given text."""
    return re.sub(r'[^\x00-\x7F]+', '', text)


def get_unified_tags(enriched_posts):
    """Unifies similar tags into broader categories using LLM."""
    unique_tags = set()
    for post in enriched_posts:
        unique_tags.update(post['tags'])

    unique_tags_list = ','.join(unique_tags)
    template = ''' I will give you list of tags. You need to unify tags with the following requirements.
    1. Tags are unified and merged to create a shorter list.
    Example 1: "Jobseekers", "Job Hunting" can all be merged into a single tag "Job Search".
    Example 2: "Motivation", "Inspiration", "Drive" can be mapped into "Motivation".
    Example 3: "Personal Growth", "Self Improvement", "Personal Development" can be merged to "Self Improvement"
    Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should follow title case convention. Example: "Job Search", "Motivation"
    3. Output should be JSON object. No preamble.
    4. Output should be mapping of original tag and unified tags. Don't miss out on any original tags.
    Example: {{"Job Seekers": "Job Search", "Job Hunting": "Job Search", "Motivation": "Motivation"}}
    
    Here is the list of tags:
    {tags}'''
    unique_tags_list = clean_text(unique_tags_list)
    prompt_template = PromptTemplate.from_template(template)
    query = prompt_template | llm
    response = query.invoke(input={'tags': str(unique_tags_list)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Content is too big. Unable to parse.")
    return res


def process_posts(raw_posts_file_path, processed_posts_file_path="data/preprocessed_posts.json"):
    """Processes raw LinkedIn posts by extracting metadata and unifying tags."""
    enriched_posts = []
    with open(raw_posts_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

        unified_tags = get_unified_tags(enriched_posts)

        # Update tags using the unified tag mapping
        for post in enriched_posts:
            current_tags = post["tags"]
            new_tags = {unified_tags[tag] for tag in current_tags}
            post["tags"] = list(new_tags)

        # Save processed posts to a new JSON file
        with open(processed_posts_file_path, encoding='utf-8', mode='w') as output_file:
            json.dump(enriched_posts, output_file, indent=4)


def extract_metadata(post):
    """Extracts metadata such as line count, language, and tags from a LinkedIn post."""
    post = clean_text(post)
    template = '''You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. Tags are an array of text tags. Extract maximum two tags.
    4. Language should be English, German or Hinglish (Hinglish means Hindi + English)
    
    Here is the actual post on which you need to perform this task:
    {post}'''

    prompt_template = PromptTemplate.from_template(template)
    query = prompt_template | llm
    response = query.invoke(input={'post': post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Content is too big. Unable to parse.")
    return res


if __name__ == "__main__":
    # Process posts from raw JSON file
    process_posts("data/raw_posts.json", "data/preprocessed_posts.json")
