import whisperx
import os
from time import time
from functools import lru_cache
files_in_directory = os.listdir("voice")
mp3_files = [f"voice/{file}" for file in files_in_directory if file.endswith('.mp3')]


@lru_cache(maxsize=None) 
def get_whisper_model(model_size="large-v2"):
	device = "cuda" 
	audio_file = "audio.mp3"
	batch_size = 16  # reduce if low on GPU mem
	compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)

	# 1. Transcribe with original whisper (batched)
	model = whisperx.load_model(model_size, device, compute_type=compute_type, language='hu')
	return model


def transcribe(filename, batch_size):
	model = get_whisper_model()
	audio = whisperx.load_audio(filename)
	res = model.transcribe(audio, batch_size=batch_size, language='hu')
	return res

def transcibe_fastwhisper():
	segments, info = audio_model.transcribe(temp_file, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=800), beam_size=5)
	text = ""
	for segment in segments:
			text += segment.text

def get_fast_whisper_model(model_name, device='auto'):
	from faster_whisper import WhisperModel
	print('model:', model_name, device)
	audio_model = WhisperModel(model_name, device=device, compute_type=compute_type, cpu_threads=cpu_threads)
	

import speech_recognition as sr
def get_record_callback(data_queue):
	def record_callback(_, audio: sr.AudioData) -> None:
		"""
		Threaded callback function to recieve audio data when recordings finish.
		audio: An AudioData containing the recorded bytes.
		"""
		# Grab the raw bytes and push it into the thread safe queue.
		data = audio.get_raw_data()
		data_queue.put(data)
	return record_callback
