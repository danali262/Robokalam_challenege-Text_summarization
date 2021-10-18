import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config


def summarize(text):
    model = T5ForConditionalGeneration.from_pretrained('t5-large')
    tokenizer = T5Tokenizer.from_pretrained('t5-large')
    device = torch.device('cpu')

    preprocess_text = text.strip().replace("\n", "")
    t5_prepared_text = "summarize: " + preprocess_text
    # print ("original text preprocessed: \n", preprocess_text)

    print("encoding with tokenizer")
    tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors="pt", max_length=512, truncation=True).to(device)
    print(len(tokenized_text[0]))

    # summarize
    print("creating model, summary ID's")
    summary_ids = model.generate(tokenized_text, num_beams=4, no_repeat_ngram_size=2, min_length=30,
                                 max_length=200, early_stopping=True)

    print("decoding tokenizer for output with summary ID's")
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("\n\nSummarized text: \n", output)

    return output
