#%%
from math import inf
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama

from tts_helper import add_text2queue, init_talk_processor

llm = Ollama(
	base_url="https://llm.sixzero.xyz", model="openhermes2.5-mistral", temperature=0.0
	# base_url="https://llm.sixzero.xyz", model="codellama:13b", temperature=0.0
	# base_url="https://llm.sixzero.xyz", model="starling-lm", temperature=0.1
)


#%%
def get_me_diff_llm(last_text, text):
	res = llm(f"""Original: '{last_text}'\n New text: {text}. \n
								The texts has a part which is similar, but I will only need the part after that similar part? The two texts are from speech, so they might have typos, which you can fix of course. Only write me new words after this sam part word by word in one line.\n """)
	return res

def is_AI_called(text, valid=None):
	res = llm(f"""Message: '{text}.'\n 
					You are an assistant. You can be called Alexa, Siri, Robot or Robi, Intelligencia, AI.  
					Your task: Decide whether you were referenced in the end of the message. Answer with 'Yes' or 'No' """ +
					  # " Please reason why you think you were mentioned. " +
					 "\n")
	if valid:  #  and not res.startswith(valid)
		print(f'{valid}:', res)
		pass
	return res.startswith("Yes")


def find_same_from_end(last_text, text):
	ltxt = last_text.lower()
	ntxt = text.lower()
	# replace all dots with one replace,
	ltxt = ltxt.replace(".", " ")
	ntxt = ntxt.replace(".", " ")
	# split by space
	ltxt = ltxt.split(" ")
	ntxt = ntxt.split(" ")
	# Start from the end of the shorter text
	min_length = min(len(ltxt), len(ntxt))
	min_cut = 9999
	min_cut_i = 9999
	# Find the index where texts start to differ
	for i in range(1, min_length + 1):
		if i>=min_cut:
			print('i>=min_cut:', i, min_cut)
			break
		for j,v in enumerate(reversed(ntxt)):
			if j>min_cut:
				break
			if ltxt[-i] == v and j<min_cut:
				min_cut = j + 1
				min_cut_i = i
				break

	# Extract the differing parts
	if min_cut == 0:
		print("LT:",last_text)
		print("TX:",text)
		return "", ""
	last_text_diff = last_text.split(" ")[-min_cut_i+1:]
	text_diff = text.split(" ")[-min_cut-1:]
	last_text_diff = ' '.join(last_text_diff)
	text_diff = ' '.join(text_diff)
	# print('difference_in_last_text:', last_text_diff)
	# print('difference_in_text:', text_diff)

	return last_text_diff, text_diff

from openai import OpenAI

client = OpenAI()

def stream_chatgpt(prompt):
	command = f"""Szia, te egy mobil asszisztens vagy, aki a mobilban működik, és a személyek kéréseire válaszolsz. A tőled telhető legjobb válaszokat próbálod mondani.\nA személy ezt mondta: {prompt}\n
	Mit reagálnál?"""
	stream = client.chat.completions.create(
		# model="gpt-4-1106-preview",
		model="gpt-3.5-turbo-1106",
		messages=[{"role": "user", "content": command}],
		stream=True,
	)
	init_talk_processor()
	for chunk in stream:
		# print(chunk.choices[0].delta.content or "", end="")
		add_text2queue(chunk.choices[0].delta.content or "")

if __name__ == "__main__":

	# LT = "Amikor ugyanaz, akkor valami tud tényleg nem stimmel. Úgyhogy most már tényleg erre kell, hogy mi a probléma."
	# TX = "Amikor ugyanaz, akkor valami tud tényleg nem stimmel. Úgyhogy most már tényleg erre kell, hogy mi a probléma. Egyáltalán."
	# print(find_same_from_end(LT, TX))
	# LT = "Amikor ugyanaz, akkor valami tud tényleg nem stimmel. Úgyhogy most már tényleg erre kell, hogy mi a probléma. Egyáltalán."
	# TX = "Amikor ugyanaz, akkor valami tud tényleg nem stimmel. Úgyhogy most már tényleg erre kell, hogy mi a probléma. Egyáltalán nem ugyanaz a kettő."
	# print(find_same_from_end(LT, TX))
	# LT = "Amikor ugyanaz, akkor valami tuti nem stimmel. Úgyhogy most már tényleg erre kell, hogy mi a probléma? Egyáltalán nem ugyanaz a kettő, amit mondod, meg amit mondjál. De, nem!"
	# TX = "Amikor ugyanaz, akkor valami tud tényleg nem stimmel. Úgyhogy most már tényleg erre kell, hogy mi a probléma. Egyáltalán nem ugyanaz a kettő, amit mondott, meg amit mondja. De, nem! Tehát akkor..."
	# print(find_same_from_end(LT, TX))
	stream_chatgpt("What is the weather like?")
