import sys
import openai
from utils import get_key

api_key = get_key()

client = openai.OpenAI(api_key = api_key)

client.files.create(
  file=open(sys.argv[1], "rb"),
  purpose="fine-tune"
)
