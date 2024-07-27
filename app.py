import gradio as gr
from openai import OpenAI
import inference
from urllib import request
import io
from PIL import Image

api_key = "..."
client = OpenAI(api_key=api_key)

PROMPT_ENGINEERING = "이제부터 판타지 rpg 게임을 만들거야. 밑에 조건들 모두 따라야만해 \
1. 맵 레벨은 적어도 3개 필요하고 쉬운단계부터 어려운 단계에서 끝내야되. \
2. 주요 퀘스트와 서브 퀘스트가 적절한 난이도로 설계하기. \
3. 보상은 다양할지만 다음 레벨로 올라가는 보상은 무조건 필요해. \
4. 게임 설명은 50-70자 적어줘 \
5. 배경은 최대한 자세하게 50-70자 적어주고 다양성이 중요해. \
6. 매번 검색은 전 세계적으로 인기를 얻었던 그리고 최신 rpg 게임을 reference로 잡고 퀘스트 만들어줘. \
7. 출력할때 적어도 50번은 전혀 일치하지 않는 내용으로 출력해줘 \
8. 이해하기 편하게 키워드도 따로 정리해줘."

def call_model(text, quest_item, event):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "넌 창의적인 판타지 RPG 게임 시나리오 작가야."},
            {"role": "user", "content": f"{PROMPT_ENGINEERING} 등장인물은 {text} 이고, 주요 이벤트는 {event}이야. 이 조건들로 3개 퀘스트 만들어줘"}
        ]
    )
    answer = completion.choices[0].message.content

    # completion = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         # {"role": "system", "content": "넌 창의적인 판타지 RPG 게임 시나리오 작가야."},
    #         {"role": "user", "content": f"{quest_item}을 하나만 영어로 알려줘"}
    #     ]
    # )
    # quest_item = completion.choices[0].message.content.split('"')[1]
    # print(quest_item)

    response = client.images.generate(
        model="dall-e-3",
        prompt=f'{quest_item}, 게임 에셋, 게임 아이템, 3d 모델 비디오 모델 에셋, 검은 배경, 화려한 색상, 판타지 게임, 고대의 스타일',
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    res = request.urlopen(image_url).read()
    quest_item = Image.open(io.BytesIO(res))

    # quest_item = inference.generate(quest_item)
    # add_prompt = ', fantasy style, high quality, game item, game icon institute, game icon,'
    # quest_item = inference.generate(quest_item + add_prompt)

    # print(completion.choices[0].message.content)
    return answer, quest_item






_HEADER_ = '''
<h2><b>🤗 StoryWeaver: 퀘스트 생성기 </b></h2><h2>
등장인물, 퀘스트 아이템, 주요 이벤트(사건)을 입력해 퀘스트 스토리를 생성해보아요!
'''


with gr.Blocks(title="AIStoryWeaver") as demo:
    gr.Markdown(_HEADER_)
    with gr.Column():
        text = gr.Textbox(label="등장인물", placeholder='등장인물의 이름을 적어주세요.')
        quest_item = gr.Textbox(label="퀘스트 아이템", placeholder='퀘스트 아이템을 적어주세요.')
        event = gr.Textbox(label="주요 이벤트(사건)", placeholder='주요 이벤트(사건)를 적어주세요.')
        submit = gr.Button("생성하기")

    with gr.Row():
        output = gr.Textbox(label="퀘스트 스토리")
        quest_item_img = gr.Image(label='퀘스트 아이템', elem_id='quest_item')

    submit.click(fn=call_model, inputs=[text, quest_item, event], outputs=[output, quest_item_img])

demo.launch(share=True)