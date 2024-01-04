# LLM assistant controlled with voice called Jarvis.

The solution:

1. Human voice from default microphone `pulse`
2. Converting it to text. Currently with `whisperx` -> `speech` 
3. Prompting a local LLM - for better latency and low cost - "If Jarvis was mentioned in the `speech` write yes." The path for local LLM: `/llms/gguf/dolphin-2.6-mistral-7b.Q5_K_M.gguf` (llm_assistant.py:10)
4. If local LLM said yes, then ChatGPT steps in and answers the question of the user.
5. We stream send the answer chunked by sentences to openAI TTS. We play the TTS.  

The host on which the script is ran can listen in discord rooms, this way anyone joining the room can speak to the host over the internet. 
To use discord as microphone:
 1. join to a discord room 
 2. Run `./mic_over_discord.sh` exposes discord channel as `pulse` default microphone. It will be available as an input device. 
 3. `main.py` will use `pulse` input device (microphone) automatically. 

# To start:

Set up your local LLM in `llm_assistant.py` on line 10: `llm = get_llm_model("/path/to/llamacpp_model-7b.Q4_K_M.gguf")`

Then run:

```bash
python3 main.py --record_timeout=1.5 --non_english --model=large-v2
```

Work in progress... Still no `requirements.txt` 

## RAG first try done.

There is a RAG connected into the system, so it can remember things you mention to the system. 