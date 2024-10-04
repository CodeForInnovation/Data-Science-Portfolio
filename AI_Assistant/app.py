import streamlit as st
from gemini import Model
from PIL import Image
# Function to simulate model responses

#using cache resource to inference the model once and use it for all the sessions
@st.cache_resource
def get_model():
    model =Model()
    return model

model = get_model()

#using cache resource and resetting the chat history for each session
@st.cache_data
def set_chat_history(_model):
    _model.set_chat()

set_chat_history(model)

st.title('AI Assitant')
if "messages" not in st.session_state:
    st.session_state['messages']=[]

#whenever user makes an interaction with app, the entire app reruns except cache values and session state.
#we are displaying the chat history of user interactions
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = []
col1, col2 = st.columns([2,4])
with col1:
    file = st.file_uploader('',type=["jpg", "jpeg", "png"])
    if file is not None:
        file_input = Image.open(file)
        prompt.append(file_input)


#displaying user's current interaction

with col2:
    if user_input := st.chat_input('How can I help you?',):
        prompt.append(user_input)
        with st.chat_message('user'):
            st.markdown(prompt)
        st.session_state['messages'].append({'role':'user','content':prompt})
        response = model.get_response(prompt)
        with st.chat_message('assistant'):
            st.markdown(response)
        st.session_state['messages'].append({'role':'assistant','content':response})