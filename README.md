# Jarvis LLM controlled with voice

Using faster-whisper for voice to text translation. The host on which the script is ran can listen in discord rooms, this way anyone joining the room can speak to the host where they are. To use discord as microphone, 1. join to a discord room 2. Run `./mic_over_discord.sh` 3. Profit. This way you will be able to access discord room voice as az input device and can use it for any purpose. 

# To start run:

```bash
python3 main.py --record_timeout=0.5 --non_english --model=large-v
```

Going to listen on first mic? I think so. Work in progress...

A Local LLM is used to determine whether "Jarvis" should speak/answer anything (To be more realtime and decrease costs by not using ChatGPT for everything). If it should then we call out to chatGPT to answer the question. 

Soon there will be a RAG connected so Jarvis will remember things you say to it.
