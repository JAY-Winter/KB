API_KEY = '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'
openai.api_key = API_KEY


def summary_GPT(request_text):
    '''
    GPT 요약 기능입니다.
    '''
    prompt_text = "한국어로 최소 1문장, 최대 50문장으로 정리하는데, '어떤 내용을 담고있는 문서입니다' 식으로 존댓말로 정리해줘 \n"
    prompt = prompt_text + request_text
    response = request_openai_summary(prompt)
    if response:
        gpt_response = response.choices[0].text.strip()
    else:
        all_tokens = [token.text for token in nlp(prompt)]
        max_tokens = 1000
        # 최대 토큰 개수를 넘지 않도록 슬라이싱
        tokens = all_tokens[:max_tokens]
        reduced_prompt = ' '.join(tokens)
        response = request_openai_summary(reduced_prompt)
    
    gpt_response = response if response else '별도의 이유로 요약되지 못 했습니다.'
    return gpt_response


def request_openai_summary(prompt):
    '''
    GPT 요약 호출 기능입니다.
    '''
    try:
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.7,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=['\n']
        )
        return response
    except openai.error.InvalidRequestError as e:
        print('error 발생',e)
        return None
