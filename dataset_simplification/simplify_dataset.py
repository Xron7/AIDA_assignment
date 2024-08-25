import openai
from utils.utils import get_key, simplify_text

api_key = get_key('../utils/api_key.txt')

client = openai.OpenAI(api_key=api_key)

text = "The cat chased the mouse, and it eventually caught it."
print(simplify_text(text, client))
