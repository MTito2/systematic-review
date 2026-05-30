from functions import construct_payload, send_openai, wait_processing, get_only_answers_unique, extract_base
import os, time
from config import RESPONSE_FOLDER, FILES_FOLDER
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# payload_path = FILES_FOLDER / "payload_content_5.jsonl"

# file = client.files.create(
#     file=open(payload_path, "rb"),
#     purpose="batch"
# )

# print(f"File id: {file.id}")

# batch = client.batches.create(
#     input_file_id=file.id,
#     endpoint="/v1/chat/completions",
#     completion_window="24h"
# )

# print(f"Batch id: {batch.id}")

# print (f"output_file_id: {batch.output_file_id}")

# while (True):
#     time.sleep(3)
#     os.system("cls")
#     batch = client.batches.retrieve("batch_6a1b0909e7e4819088a7c8b30363d556")
#     print(batch.status)
#     print(batch.output_file_id)

get_only_answers_unique("file-WxW8CFuPFYgBeYLu67YTWC")
