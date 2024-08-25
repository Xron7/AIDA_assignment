import sys
import openai
from utils import get_key

api_key = get_key()

client = openai.OpenAI(api_key = api_key)

client.fine_tuning.jobs.create(
  training_file=sys.argv[1],
  model="gpt-4o-mini-2024-07-18"
)
