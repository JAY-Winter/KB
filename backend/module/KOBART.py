import torch
from kobart_transformers import get_kobart_tokenizer


def summary_KOBART(text, model, tokenizer):
    '''
    KO-BART 모델로 text 를 요약합니다.
    '''
    input_ids = tokenizer.encode(text)
    input_ids = torch.tensor(input_ids)
    input_ids = input_ids.unsqueeze(0)
    output = model.generate(input_ids, eos_token_id=1, max_length=1024, num_beams=5)
    output = tokenizer.decode(output[0], skip_special_tokens=True)
    return output