# Auto Software developer

**Prerequisites:**

- `Ollama` - install from [here](https://ollama.com/download/linux)
- `uv` - install from [here](https://docs.astral.sh/uv/#installation)

Check your installations by running these commands in your terminal.
```bash
ollama -v  # ollama version is 0.33.1
uv --version  # uv 0.12.7 (x86_64-unknown-linux-gnu)
```

- Make sure you have pulled the LLM models from ollama and they are ready on your machine. Run the following command to pull the models.

```bash
ollama pull "model_1" "model_2" ...
ollama list
```
- Make a `.env` file and add your LLM models. You can re-use the recommended models from `.env-example` file

**Run the code:**

Run the project following on-screen prompts.
```bash
uv run main.py
```