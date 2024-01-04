import argparse
import io, os
import speech_recognition as sr
from pathlib import Path
from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep, time
from sys import platform

from llm_assistant import find_same_from_end, is_AI_called, is_AI_called_Jarvis, stream_chatgpt, stream_chatgpt_single
from speech_recorder import get_mic_source
from stt_helper import get_record_callback, transcribe
from tts_helper import add_text2queue, wait_for_speech_sleep


def main():
    
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="medium", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large-v2", "large"])
    parser.add_argument("--device", default="auto", help="device to user for Whisper inference",
                        choices=["auto", "cuda","cpu"])                   
    parser.add_argument("--compute_type", default="auto", help="Type of quantization to use",
                        choices=["auto", "int8", "int8_floatt16", "float16", "int16", "float32"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the english model.")
    parser.add_argument("--threads", default=0,
                        help="number of threads used for CPU inference", type=int)
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=1,
                        help="How real time the recording is in seconds.", type=float)
                        
    parser.add_argument("--phrase_timeout", default=3,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float) 
                             
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()
    
    model = args.model
    # if args.model == "large":
        # args.model = "large-v2"    
    if args.model != "large-v2" and not args.non_english:
        model = model + ".en"
         
    device = args.device
    if device == "cpu":
        compute_type = "int8"
    else:
        compute_type = args.compute_type
    cpu_threads = args.threads
    
    # Current raw audio bytes.
    last_sample = []

    sound_chunk_threshold = 10
    last_text = ""
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False
    
    source = get_mic_source(args.default_microphone)
    
    record_timeout = args.record_timeout
    phrase_timeout = args.phrase_timeout

    with source:
        recorder.adjust_for_ambient_noise(source)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, get_record_callback(data_queue), phrase_time_limit=record_timeout)
    # Cue the user that we're ready to go.

    # temp_file = NamedTemporaryFile().name
    temp_file = Path(__file__).parent / "voice" / "tmp_recording.mp3"
    print("Model loaded.\n")
    add_text2queue("Figyelek! Jöhetnek a kérdések.")
    

    while True:
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                phrase_complete = False
                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                # if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                #     last_sample = bytes()
                #     phrase_complete = True
                # This is the last time we received new audio data from the queue.
                # phrase_time = now

                # Concatenate our current audio data with the latest audio data.
                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += [data]
                last_sample = last_sample[-sound_chunk_threshold:]
                # concat list of bytes together into one big bytes array
                full_data = b''.join(last_sample)

                
                wav_convert_time = time()
                # Use AudioData to convert the raw data to wav data.
                audio_data = sr.AudioData(full_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                wav_data = io.BytesIO(audio_data.get_wav_data())
                # print('wav_conversion_time:', time() - wav_convert_time)
                # Write wav data to the temporary file as bytes.
                wav_convert_time = time()
                with open(temp_file, 'w+b') as f:
                    f.write(wav_data.read())
                # print(f'wav_write: {time() - wav_convert_time:.2f}', )

                # Read the transcription.
                f_time = time()
                BATCH_SIZE=16
                res = transcribe(temp_file, batch_size=BATCH_SIZE)
                stt_time = time() - f_time 
                if len(res['segments']) > 1:
                    print("WHHHHYYYY", [(t["start"], t["end"]) for t in res['segments']])
                if len(res["segments"]) == 0:
                    continue
                text = res['segments'][-1]['text']
                
                # print('last_text =', last_text)
                # print('->', find_same_from_end(last_text, text))
                print(f"text = '{text}'")
                llm_time = time()
                if len(last_sample) > 4 and is_AI_called_Jarvis(text):
                    add_text2queue("Egy pillanat.")

                    print('YES AI reguested:', )
                    # call openai chatGPT 4 for answer with langchain
                    # res = stream_chatgpt_single(text.strip())
                    res = stream_chatgpt(text.strip())
                    wait_for_speech_sleep()
                    if "Silent" != res:
                        print("We reset what we heard in the meantime!")
                        last_sample = [] # maybe keep the last sample.
                        while not data_queue.empty():
                            data = data_queue.get()
                    elif len(last_sample) > 5:
                        last_sample = last_sample[-5:]
                    pass
                
                llm_elapsed = time() - llm_time
                #text = result['text'].strip()
                print(f"STT: {stt_time:.2f}s LLM: {llm_elapsed:.2f}s", "" if len(last_sample)>29 else f"{len(last_sample)}/{sound_chunk_threshold}")

                last_text = text

                # Infinite loops are bad for processors, must sleep.
        except KeyboardInterrupt:
            break
        sleep(0.05)



if __name__ == "__main__":
    
    main()
