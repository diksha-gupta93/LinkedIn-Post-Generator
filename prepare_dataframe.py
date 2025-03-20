import json
import pandas as pd


class DataFrameBuilder:
    """Handles loading and filtering posts for LinkedIn post generation."""
    def __init__(self, file_path="data/preprocessed_posts.json"):
        """Initializes DataFrameBuilder by loading posts from a JSON file."""
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        """Loads posts from the JSON file and processes data."""
        with open(file_path, encoding="utf-8") as file:
            posts = json.load(file)
            self.df = pd.json_normalize(posts)
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)
            all_tags = self.df["tags"].apply(lambda x: x).sum()
            self.unique_tags = set(list(all_tags))

    def categorize_length(self, length_count):
        """Categorizes posts into Short, Medium, or Long based on line count."""
        if length_count < 5:
            return "Short"
        elif 5 < length_count < 10:
            return "Medium"
        else:
            return "Long"

    def get_filtered_posts(self, length, language, tag):
        """Filters posts based on length, language, and tag."""
        filtered_posts = self.df[
            (self.df["language"] == language) &
            (self.df["length"] == length) &
            (self.df["tags"].apply(lambda tags: tag in tags))
        ]
        return filtered_posts.to_dict(orient="records")

    def get_tags(self):
        """Returns a set of unique tags from the dataset."""
        return self.unique_tags


if __name__ == "__main__":
    # Example
    fs = DataFrameBuilder()
    posts = fs.get_filtered_posts("Medium", "English", "Job Search")
    print(posts)
