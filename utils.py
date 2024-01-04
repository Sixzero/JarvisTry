import json

def load_jsonl(filename):
	with open(filename) as f:
		data = [json.loads(line) for line in f]
	return data

def write_jsonl(filename, data):
	# Write data to JSONL file
	with open(filename, 'w') as file:
			for entry in data:
					# Convert dictionary to JSON string and write to file
					file.write(json.dumps(entry) + '\n')

def append_jsonl(filename, new_data_line):
    with open(filename, 'a') as file:
        # Convert dictionary to JSON string and write to file
        file.write(json.dumps(new_data_line) + '\n')