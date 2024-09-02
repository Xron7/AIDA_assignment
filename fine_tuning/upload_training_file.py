import sys
import openai
from utils.utils import get_key

#
# argument is the csv file (pipe-separated) containing the samples
#

api_key = get_key('../utils/api_key.txt')

client = openai.OpenAI(api_key = api_key)

client.files.create(
  file=open(sys.argv[1], "rb"),
  purpose="fine-tune"
)
