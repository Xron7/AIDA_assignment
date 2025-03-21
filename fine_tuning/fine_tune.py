import sys
import openai
from utils.utils import get_key

#
# argument is the uploaded file id (visible in the Storage of the Dashboard)
#
#
# submits a job for fine-tuning a gpt model
#

api_key = get_key('../utils/api_key.txt')

client = openai.OpenAI(api_key = api_key)

client.fine_tuning.jobs.create(
  training_file=sys.argv[1],
  model="gpt-4o-mini-2024-07-18"
)
