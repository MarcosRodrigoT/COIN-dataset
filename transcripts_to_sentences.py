import glob
import requests
import json


def get_full_sentence(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": "llama3", "prompt": prompt, "stream": False}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        return result["response"].strip()
    else:
        print(f"Error: {response.status_code}")
        return ""


def process_clean_transcript(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Append all sentences to a list
    sentences = []
    for line in lines:
        line = line.strip()
        if line:
            sentences.append(line)

    # Convert the list of sentences into a continuous text
    text = " ".join(sentences)

    with open(output_file, "w", encoding="utf-8") as file:
        full_sentences = get_full_sentence(
            "Separate the following text into full sentences. Write each full sentence in a new line. Do not create a numbered list,"
            " simply output each full sentence in a new line. Refrain from adding any comments such as 'Here are the full sentences:' in"
            " your response. Simply add punctuation marks where necessary and use upper/lower case letters where necessary. Here is the"
            f" text: {text}"
        )

        file.write(full_sentences)


if __name__ == "__main__":
    for clean_transcript in sorted(glob.glob("transcripts/*/*_wo_timestamps.txt")):
        print(f"Processing file: {clean_transcript}")

        output_file = f"{clean_transcript.split('_wo_timestamps')[0]}_sentences.txt"
        process_clean_transcript(clean_transcript, output_file)
