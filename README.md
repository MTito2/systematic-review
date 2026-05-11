# Batch Processing com OpenAI API

Sistema em Python para processamento em lote de artigos utilizando a API da OpenAI.  
O projeto lê uma base Excel, filtra artigos elegíveis, monta arquivos `.jsonl` para Batch Processing, envia os batches para a OpenAI e exporta as respostas em `.json` e `.xlsx`.

---

# Funcionalidades

- Leitura de arquivos `.json`, `.jsonl` e `.txt`
- Exportação de dados em `.json`, `.txt` e `.xlsx`
- Filtragem de artigos diretamente de uma planilha Excel
- Construção automática de payloads para Batch API
- Divisão automática dos artigos em 5 batches
- Envio automatizado para a OpenAI
- Monitoramento do status dos batches
- Extração e organização das respostas
- Exportação final em Excel e JSON

---

# Tecnologias Utilizadas

- Python
- Pandas
- OpenAI API
- python-dotenv

---

# Estrutura do Projeto

```bash
project/
│
├── config.py
├── main.py
├── .env
│
├── files/
│   ├── base_origin.xlsx
│   ├── prompt.txt
│   ├── payload_content_1.jsonl
│   ├── payload_content_2.jsonl
│   └── ...
│
├── responses/
│   ├── response_1.json
│   ├── response_1.xlsx
│   └── ...
```

---

# Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

Entre na pasta:

```bash
cd seu-repositorio
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

# Dependências

Exemplo de `requirements.txt`:

```txt
openai
pandas
python-dotenv
openpyxl
```

---

# Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_api
```

---

# Configuração do `config.py`

Exemplo:

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

FILES_FOLDER = BASE_DIR / "files"
RESPONSE_FOLDER = BASE_DIR / "responses"
```

---

# Estrutura da Base Excel

A planilha deve conter:

| Coluna | Descrição |
|---|---|
| TI | Título do artigo |
| AB | Resumo do artigo |
| Elegibilidade | Campo utilizado para filtragem |

O script filtra apenas linhas onde:

```python
Elegibilidade == NaN
```

---

# Fluxo do Projeto

## 1. Construir os payloads

```python
construct_payload()
```

Essa etapa:

- lê a planilha
- monta os prompts
- cria os arquivos `.jsonl`
- divide automaticamente em 5 batches

---

## 2. Enviar batches para OpenAI

```python
send_openai()
```

Essa função:

- faz upload dos arquivos `.jsonl`
- cria os batches
- salva os IDs em `batches.txt`

---

## 3. Monitorar processamento

```python
wait_processing()
```

O script consulta continuamente o status dos batches até:

- completed
- failed
- cancelled

---

## 4. Exportar respostas

Todos os batches:

```python
get_only_answers()
```

Ou apenas um batch específico:

```python
get_only_answers_unique(output_id)
```

---

# Modelo Utilizado

```python
gpt-5.4-mini
```

Temperatura:

```python
0.2
```

---

# Exemplo de Payload

```json
{
  "custom_id": "artigo_15",
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "gpt-5.4-mini",
    "messages": [
      {
        "role": "system",
        "content": "Seu prompt"
      },
      {
        "role": "user",
        "content": "Título: ...\nResumo: ..."
      }
    ],
    "temperature": 0.2
  }
}
```

---

# Saída Gerada

## JSON

```json
[
  {
    "id": "artigo_1",
    "resposta": "Resposta do modelo"
  }
]
```

## Excel

| id | resposta |
|---|---|
| artigo_1 | Resposta do modelo |

---

# Possíveis Melhorias

- Paralelização do monitoramento
- Retry automático para batches falhos
- Logs estruturados
- Interface gráfica
- Integração com banco de dados
- Configuração dinâmica da quantidade de batches

---

# Licença

Este projeto está sob a licença MIT.
