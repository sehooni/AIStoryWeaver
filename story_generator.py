import streamlit as st
# # from transformers import pipeline
# from langchain.chat_models import ChatOpenAI
# from langchain.schema import AIMessage, HumanMessage, SystemMessage

import openai
import os

# # 발급받은 API 키 설정
OPENAI_API_KEY = "..."

# # openai API 키 인증
openai.api_key = OPENAI_API_KEY
# os.environ["OPENAI_API_KEY"] = "..." 




# # Load the model with caching
# @st.cache(allow_output_mutation=True)
# def load_model():
#     model = pipeline('text-generation', model='gpt2')
#     return model

def load_model(query, temperature):
    # 모델 - GPT 3.5 Turbo 선택
    model = "gpt-3.5-turbo"

    # 메시지 설정하기
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
    }, {
        "role": "user",
        "content": query,
        "temperature": temperature
    }]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    answer = response['choices'][0]['message']['content']
    
    return answer
    

# story_generator = load_model()

st.title('Interactive Short-Story Creator')

# Genre selection
genre = st.selectbox(
    "Choose the genre of your story:",
    ('판타지', '공상과학', '미스터리', '호러', '어드벤처', '멜로', '로맨스')
)

# Additional inputs for a more tailored story
character = st.text_input("Enter a main character name:")
setting = st.text_input("Enter a setting (e.g., a magical forest, a spaceship):")
user_input = st.text_area("Start your story here...:")

# Advanced configuration options
# max_length = st.slider("Select the length of the story continuation:", 100, 1000, 500)
temperature = st.slider("Adjust creativity of the story:", 0.7, 1.5, 1.0)

if st.button('Generate Story Continuation'):
    with st.spinner('AI is writing the story...'):
        # Improved prompt construction with user inputs
        prompt = f"장르: {genre}.\n 주인공: {character}.\n 설정: {setting}.\n 스토리 시작 : '{user_input}'"
        
        try:
            generated_story = load_model(prompt, temperature=temperature)
            st.text_area("Here's the continuation of your story:", generated_story, height=250)
        except Exception as e:
            st.error(f"Error generating story: {str(e)}")

# Collecting user feedback
feedback = st.text_area("Feedback on the generated story:", "")
if st.button('Submit Feedback'):
    st.write("Thanks for your feedback!")
