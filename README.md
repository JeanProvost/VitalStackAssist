# VitalStackAssist

VitalStackAssist is a Python-based FastAPI service that orchestrates large language models (LLMs)
to analyze potential interactions, synergies, and risk factors across dietary supplement stacks.
This README walks you through setting up the project locally so you can experiment with model
configurations before deploying to environments that use providers such as AWS Bedrock.

## 1. Prerequisites

Make sure the following tooling is installed on your machine:

- [Python 3.11+](https://www.python.org/downloads/) (3.11 is recommended)
- [Git](https://git-scm.com/downloads)
- (Optional) [virtualenv](https://virtualenv.pypa.io/en/latest/) or
  [uv](https://github.com/astral-sh/uv) if you prefer isolated environments
- (Optional) An OpenAI-compatible local LLM runtime such as [vLLM](https://github.com/vllm-project/vllm),
  [LM Studio](https://lmstudio.ai/), or [Ollama](https://ollama.com/) with the OpenAI bridge enabled

## 2. Clone the Repository

```powershell
cd C:\path\to\your\workspace
git clone https://github.com/JeanProvost/VitalStackAssist.git
cd VitalStackAssist
```

## 3. Create and Activate a Virtual Environment (Recommended)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

If you use an alternative environment manager, adjust the commands accordingly.

## 4. Install Python Dependencies

Install the required packages (including `boto3`, which is used when targeting AWS Bedrock):

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Environment Variables

The project ships with a sample `.env.local` file that is loaded automatically by the
configuration layer. Copy it to `.env` (or leave it as `.env.local`) and update the values
based on the provider you plan to use.

```powershell
Copy-Item .env.local .env
```

### Local OpenAI-Compatible Runtime (default)

By default, the configuration targets a local OpenAI-compatible endpoint listening on
`http://127.0.0.1:8000/v1` and uses the `meta-llama/Llama-3.1-8B-Instruct` model identifier.
If your runtime requires an API key, set `LOCAL_API_KEY`. Otherwise you can unset the variable.

### OpenAI Platform

Uncomment and populate the following variables in `.env`:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_BASE=https://api.openai.com/v1
```

### AWS Bedrock

Install and configure the AWS CLI with credentials that have Bedrock access, then set:

```
LLM_PROVIDER=bedrock
BEDROCK_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
BEDROCK_PROFILE=default
# Optional overrides
BEDROCK_ENDPOINT_URL=https://bedrock-runtime.us-east-1.amazonaws.com
BEDROCK_MAX_TOKENS=2048
BEDROCK_TEMPERATURE=0.2
```

## 6. (Optional) Start a Local LLM Runtime

To run the interaction analysis end-to-end without external dependencies, launch an
OpenAI-compatible server locally. Example using LM Studio (UI configuration) or vLLM CLI:

```powershell
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --host 127.0.0.1 --port 8000
```

Adjust the command or model name to match your tooling.

## 7. Run the FastAPI Application

Use Uvicorn to start the API locally:

```powershell
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 9000
```

The service will be available at `http://127.0.0.1:9000`. Interactive API docs are served from
`http://127.0.0.1:9000/docs`.

## 8. Trigger an Interaction Analysis

Send a request with your supplement stack. Example using `curl`:

```powershell
curl -X POST "http://127.0.0.1:9000/generate-interactions" \
     -H "Content-Type: application/json" \
     -d '{
           "supplements": ["magnesium", "vitamin d"],
           "biomarkers": ["serum calcium"],
           "goals": ["bone health"]
         }'
```

The response structure is defined in `src/models/interaction.py` and includes conflicts,
synergies, depletions, optimizations, and dosage warnings.

## 9. Switching Providers During Development

The configuration system exposes a single environment variable `LLM_PROVIDER` that can be set to
`local`, `openai`, or `bedrock`. Provider-specific parameters are validated at startup so the
service fails fast if required values are missing. Update `.env` and reload the server to target a
different provider.

## 10. Running Tests

The repository does not currently include automated tests. When adding new functionality, follow the
project guidelines and add unit tests alongside the relevant modules.

## 11. Troubleshooting

- Ensure your environment file (`.env` or `.env.local`) is accessible and uses UTF-8 encoding.
- When targeting Bedrock, guarantee that the AWS credentials have the `bedrock:*` permissions and
  that `boto3` can locate the desired profile.
- For local providers, confirm the server exposes the `/v1/chat/completions` endpoint.
- Review `src/ai/client.py` for detailed provider logic if you need to extend or debug the transport layer.

## 12. Next Steps

- Finalize the system prompt in `.env` once clinical requirements are defined.
- Expand the data models in `src/models/interaction.py` to capture additional insights as needed.
- Add automated tests and deployment workflows when you are ready to promote the service beyond local development.
