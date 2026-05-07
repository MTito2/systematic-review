import os, json, time
import pandas as pd
from config import FILES_FOLDER
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def read_json(name_path, name_file: str):
    name_json_file = name_path / name_file

    with open(name_json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data
        
def read_jsonl(name_path, name_file: str):
    name_jsonl_file = name_path / name_file
    data = []

    with open(name_jsonl_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def export_json(content, name_path, name_file="content.json") -> None:
    name_json_file = name_path / name_file

    with open(name_json_file, "w", encoding="utf-8") as file:
        json.dump(content, file, indent=4, ensure_ascii=False)

def export_txt(content, name_path, name_file, type) :
    name_file_txt = name_path / name_file

    with open(name_file_txt, type, encoding="utf-8") as file:
        file.writelines(f"{content}\n")

def read_txt(name_path, name_file) :
    name_file_txt = name_path / name_file

    with open(name_file_txt, "r", encoding="utf-8") as file:
        content = file.read()

    return set(content.split("\n")[:-1])

def clean_txt(file_name):
    file_name = FILES_FOLDER / file_name
    open(file_name, "w").close()


def extract_base():
    df = pd.read_excel(FILES_FOLDER / "base_origin.xlsx", sheet_name="Base_Presos (2)")
    df = df[df['Elegibilidade'].isna()]
    df = df[["TI", "AB"]]
    df.to_excel(FILES_FOLDER / "base_formatted.xlsx")
    return df
    
def construct_payload():
    df = extract_base()

    prompt_path = FILES_FOLDER / "prompt.txt"

    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read()

    content = []

    for index, row in df.iterrows():
        article_content = f"Título: {row['TI']}\nResumo: {row['AB']}"
        custom_id = f"artigo_{index}"

        row_batch = {
            "custom_id": custom_id,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-5.4-mini", 
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": article_content}
                ],
                "temperature": 0.2 
            }
        }

        content.append(row_batch)

    articles_division = len(content)
    base = articles_division // 5
    rest = articles_division % 5
    parts = [base] * 5
    for i in range(rest):
        parts[i] += 1

    couter_articles = 1
    
    result = []
    start = 0

    for size in parts:
        end = start + size
        result.append(content[start:end])
        start = end
    
    for item in result:
        payload_path = FILES_FOLDER / f"payload_content_{couter_articles}.jsonl"
  
        with open(payload_path, "w", encoding="utf-8") as f:
            for row in item:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        couter_articles += 1

def send_openai():
    clean_txt("batches.txt")
    
    for i in range(5):
        payload_path = FILES_FOLDER / f"payload_content_{i + 1}.jsonl"

        my_file = client.files.create(
            file=open(payload_path, "rb"),
            purpose="batch"
        )

        file_id = my_file.id

        batch = client.batches.create(
            input_file_id=file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h"
        )

        
        export_txt(batch.id, FILES_FOLDER, "batches.txt", "a")

def wait_processing():
    status = "validating"

    while status not in ["failed", "completed", "cancelled"]:
        time.sleep(10)
        os.system("cls")
        
        batches = read_txt(FILES_FOLDER, "batches.txt")

        for batch_id in batches:
            batch = client.batches.retrieve(batch_id)
            status = batch.status
            print(f"Id: {batch_id}")
            print(f"Status: {status}")
            print()


            if status in ["processed", "completed"]:
                export_txt(batch.output_file_idutputs, FILES_FOLDER, "batch_output_id.txt", "a")



def get_only_answers():
    output_file_id = wait_processing()
    file = client.files.content(output_file_id)

    responses = []

    for line in file.text.splitlines():
        data = json.loads(line)
        
        content = data["response"]["body"]["choices"][0]["message"]["content"]
        custom_id = data["custom_id"]

        responses.append({
            "id": custom_id,
            "resposta": content
        })

    export_json(responses, FILES_FOLDER, "response.json")
    df = pd.DataFrame(responses)
    df.to_excel(FILES_FOLDER / "response.xlsx")

send_openai()
wait_processing()
