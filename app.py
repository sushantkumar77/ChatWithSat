# import streamlit as st
# import os
# import tempfile
# import pdfplumber
# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import create_retrieval_chain
# from langchain_community.vectorstores import DocArrayInMemorySearch
# from langchain_core.documents import Document
# from dotenv import load_dotenv
#
# load_dotenv()
# groq_api_key ="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"
#
# st.markdown(
#     """
#     <h2 style='text-align: center;'>AI QueryBot [Sushant Kumar (VIT Vellore: 21BCI0321)]</h2>
#     <p style='text-align: center; font-size: 16px;'>
#         Upload a PDF, ask questions from it, and get answers in your preferred language.
#         <br><br>
#         🌐 <strong>Supports 30+ Languages</strong>:<br>
#         English, Hindi, Marathi, Tamil, Telugu, Kannada, Punjabi, Gujarati, Bengali, Bhojpuri, Urdu<br>
#         Spanish, French, German, Italian, Portuguese, Dutch, Arabic, Russian, Chinese, Japanese, Korean and more.
#         <br><br>
#         🔊 <em>Voice updates are coming soon. Stay tuned!</em>
#     </p>
#     """,
#     unsafe_allow_html=True
# )
#
#
#
# prompt = ChatPromptTemplate.from_template(
#     """
#     You are a multilingual expert AI assistant. Use ONLY the information provided in the context (extracted from the PDF) to answer user questions.
#
# 1. Search the entire context thoroughly before responding.
# 2. If the information is found, answer clearly and concisely, using the same language as the question.
# 3. If the answer is partially available, explain using what you found and clearly state the limitation.
# 4. If the answer is completely missing, reply: "Please contact 6203027188 for further information."
# 5. Whenever possible, cite or refer to the relevant section or topic in the PDF.
#
# Always maintain a helpful, professional, and respectful tone.
#
#
#     <context>
#     {context}
#     </context>
#     Question: {input}
#     """
# )
#
# llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")
#
# def is_out_of_context(answer):
#     keywords = [
#         "i'm sorry", "i don't know", "not sure", "out of context",
#         "invalid", "no mention"
#     ]
#     return any(k in answer.lower() for k in keywords)
#
# def extract_text_with_pdfplumber(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"
#     return text
#
# def initialize_vector_db(pdf_file):
#     if "vector_store" not in st.session_state:
#         try:
#             with st.spinner("Reading and processing PDF..."):
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
#                     temp_file.write(pdf_file.read())
#                     pdf_path = temp_file.name
#
#                 text_data = extract_text_with_pdfplumber(pdf_path)
#
#                 if not text_data.strip():
#                     st.error("PDF appears empty or unreadable.")
#                     return False
#
#                 doc = Document(page_content=text_data)
#                 text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
#                 chunks = text_splitter.split_documents([doc])
#
#                 st.session_state.embeddings = HuggingFaceEmbeddings(
#                     model_name='sentence-transformers/distiluse-base-multilingual-cased-v2',
#                     model_kwargs={'device': 'cpu'},
#                     encode_kwargs={'normalize_embeddings': True}
#                 )
#
#                 st.session_state.vector_store = DocArrayInMemorySearch.from_documents(
#                     chunks, st.session_state.embeddings
#                 )
#
#                 os.unlink(pdf_path)
#
#             st.success("PDF has been successfully loaded!")
#             return True
#
#         except Exception as e:
#             st.error(f"Error: {str(e)}")
#             return False
#     return True
#
# # Initialize chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
#
# # PDF Upload section
# pdf_input_from_user = st.file_uploader("Please upload your multilingual PDF file", type=['pdf'])
#
# if pdf_input_from_user is not None:
#     if st.button("Process PDF"):
#         if initialize_vector_db(pdf_input_from_user):
#             st.success("Ready to chat!")
#
# # Chat interface
# if "vector_store" in st.session_state:
#     st.subheader("Chat History")
#     for msg in st.session_state.chat_history:
#         role = "**You:**" if msg["role"] == "user" else "**Bot:**"
#         st.write(f"{role} {msg['content']}")
#         st.write("---")
#
#     user_prompt = st.text_input("Enter your question in any language:")
#
#     if st.button("Send Message"):
#         if user_prompt:
#             st.session_state.chat_history.append({"role": "user", "content": user_prompt})
#
#             with st.spinner("Getting answer..."):
#                 document_chain = create_stuff_documents_chain(llm, prompt)
#                 retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 5})
#                 retrieval_chain = create_retrieval_chain(retriever, document_chain)
#
#                 response = retrieval_chain.invoke({'input': user_prompt})
#                 answer = response['answer']
#
#                 if is_out_of_context(answer):
#                     answer = "I'm sorry, the answer is not available in the provided document."
#
#                 st.session_state.chat_history.append({"role": "assistant", "content": answer})
#                 st.experimental_rerun()
#         else:
#             st.error("Please enter a question.")
# else:
#     st.info("Upload and process a PDF to start chatting.")



# import streamlit as st
# import os
# import tempfile
# import pdfplumber
# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import create_retrieval_chain
# from langchain_community.vectorstores import DocArrayInMemorySearch
# from langchain_core.documents import Document
# from dotenv import load_dotenv

# load_dotenv()
# groq_api_key = "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"

# st.markdown(
#     """
#     <h2 style='text-align: center;'>AI QueryBot [Sushant Kumar (VIT Vellore: 21BCI0321)]</h2>
#     <p style='text-align: center; font-size: 16px;'>
#         Upload a PDF, ask questions from it, and get answers in your preferred language.
#         <br><br>
#         🌐 <strong>Supports 30+ Languages</strong>:<br>
#         English, Hindi, Marathi, Tamil, Telugu, Kannada, Punjabi, Gujarati, Bengali, Bhojpuri, Urdu<br>
#         Spanish, French, German, Italian, Portuguese, Dutch, Arabic, Russian, Chinese, Japanese, Korean and more.
#         <br><br>
#         🔊 <em>Voice updates are coming soon. Stay tuned!</em>
#     </p>
#     """,
#     unsafe_allow_html=True
# )

# prompt = ChatPromptTemplate.from_template(
#     """
#     You are a multilingual expert AI assistant. Use ONLY the information provided in the context (extracted from the PDF) to answer user questions.

# 1. Search the entire context thoroughly before responding.
# 2. If the information is found, answer clearly and concisely, using the same language as the question.
# 3. If the answer is partially available, explain using what you found and clearly state the limitation.
# 4. If the answer is completely missing, reply: "Please contact 6203027188 for further information."
# 5. Whenever possible, cite or refer to the relevant section or topic in the PDF.

# Always maintain a helpful, professional, and respectful tone.

#     <context>
#     {context}
#     </context>
#     Question: {input}
#     """
# )

# llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# def is_out_of_context(answer):
#     keywords = [
#         "i'm sorry", "i don't know", "not sure", "out of context",
#         "invalid", "no mention"
#     ]
#     return any(k in answer.lower() for k in keywords)

# def extract_text_with_pdfplumber(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"
#     return text

# def initialize_vector_db(pdf_file):
#     if "vector_store" not in st.session_state:
#         try:
#             with st.spinner("Reading and processing PDF..."):
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
#                     temp_file.write(pdf_file.read())
#                     pdf_path = temp_file.name

#                 text_data = extract_text_with_pdfplumber(pdf_path)

#                 if not text_data.strip():
#                     st.error("PDF appears empty or unreadable.")
#                     return False

#                 doc = Document(page_content=text_data)
#                 text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
#                 chunks = text_splitter.split_documents([doc])

#                 st.session_state.embeddings = HuggingFaceEmbeddings(
#                     model_name='sentence-transformers/distiluse-base-multilingual-cased-v2',
#                     model_kwargs={'device': 'cpu'},
#                     encode_kwargs={'normalize_embeddings': True}
#                 )

#                 st.session_state.vector_store = DocArrayInMemorySearch.from_documents(
#                     chunks, st.session_state.embeddings
#                 )

#                 os.unlink(pdf_path)

#             st.success("PDF has been successfully loaded!")
#             return True

#         except Exception as e:
#             st.error(f"Error: {str(e)}")
#             return False
#     return True

# # Initialize chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # ✅ Auto-load PDF from same folder instead of asking for upload
# default_pdf_path = "SatyuktQueries.pdf"  # Change this filename to your actual PDF
# if os.path.exists(default_pdf_path):
#     class DummyFile:
#         def read(self):
#             with open(default_pdf_path, "rb") as f:
#                 return f.read()
#     pdf_input_from_user = DummyFile()

#     if initialize_vector_db(pdf_input_from_user):
#         st.success(f"'{default_pdf_path}' loaded successfully! You can now start chatting.")
# else:
#     st.error(f"PDF file '{default_pdf_path}' not found in the project directory.")

# # Chat interface
# if "vector_store" in st.session_state:
#     st.subheader("Chat History")
#     for msg in st.session_state.chat_history:
#         role = "**You:**" if msg["role"] == "user" else "**Bot:**"
#         st.write(f"{role} {msg['content']}")
#         st.write("---")

#     user_prompt = st.text_input("Enter your question in any language:")

#     if st.button("Send Message"):
#         if user_prompt:
#             st.session_state.chat_history.append({"role": "user", "content": user_prompt})

#             with st.spinner("Getting answer..."):
#                 document_chain = create_stuff_documents_chain(llm, prompt)
#                 retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 5})
#                 retrieval_chain = create_retrieval_chain(retriever, document_chain)

#                 response = retrieval_chain.invoke({'input': user_prompt})
#                 answer = response['answer']

#                 if is_out_of_context(answer):
#                     answer = "I'm sorry, the answer is not available in the provided document."

#                 st.session_state.chat_history.append({"role": "assistant", "content": answer})
#                 st.experimental_rerun()
#         else:
#             st.error("Please enter a question.")
# else:
#     st.info("Waiting for PDF to load...")





import streamlit as st
import os
import tempfile
import pdfplumber
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()
groq_api_key = "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"

st.markdown(
    """
    <h2 style='text-align: center;'>🌾 Welcome to Satyukt Analytics Virtual Assistant</h2>
    <p style='text-align: center; font-size: 16px;'>
        Empowering Agriculture with Satellite Intelligence & AI 🚀<br><br>
        
        I'm your smart assistant, here to help you explore how Satyukt can support your farming, finance, insurance, or agri-business needs.<br><br>

        💼 <strong>Ask me about:</strong><br>
        Sat2Farm, Sat2Credit, Sat2Farm<br>
        Crop monitoring • Weather advisory • Credit & risk analytics • Agri-insurance claims • Custom solutions<br><br>

        🌍 <strong>Precision Agriculture for Everyone:</strong><br>
        From individual farmers to banks, insurers, FPOs & governments — we’ve got you covered.<br><br>

        🔊 <em>Multilingual & Voice-enabled support coming soon!</em><br>
        🌐 <strong>Available in 30+ Languages</strong><br>
         English •Hindi • Kannada • Tamil • Telugu • Bengali • Marathi • Gujarati • Punjabi • Bhojpuri • and more!
    </p>
    """,
    unsafe_allow_html=True
)


prompt = ChatPromptTemplate.from_template(
    """
    You are a multilingual expert AI assistant. Use ONLY the information provided in the context (extracted from the PDF) to answer user questions.

1. Search the entire context thoroughly before responding.
2. If the information is found, answer clearly and concisely, using the same language as the question.
3. If the answer is partially available, explain using what you found and clearly state the limitation.
4. If the answer is completely missing, reply: "Please contact 6203027188 for further information."
5. Whenever possible, cite or refer to the relevant section or topic in the PDF.

Always maintain a helpful, professional, and respectful tone.

    <context>
    {context}
    </context>
    Question: {input}
    """
)

llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

def is_out_of_context(answer):
    keywords = [
        "i'm sorry", "i don't know", "not sure", "out of context",
        "invalid", "no mention"
    ]
    return any(k in answer.lower() for k in keywords)

def extract_text_with_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def initialize_vector_db(pdf_file):
    if "vector_store" not in st.session_state:
        try:
            with st.spinner("Hang tight! We’re connecting you to our Virtual Assistant"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(pdf_file.read())
                    pdf_path = temp_file.name

                text_data = extract_text_with_pdfplumber(pdf_path)

                if not text_data.strip():
                    st.error("PDF appears empty or unreadable.")
                    return False

                doc = Document(page_content=text_data)
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
                chunks = text_splitter.split_documents([doc])

                st.session_state.embeddings = HuggingFaceEmbeddings(
                    model_name='sentence-transformers/distiluse-base-multilingual-cased-v2',
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )

                st.session_state.vector_store = DocArrayInMemorySearch.from_documents(
                    chunks, st.session_state.embeddings
                )

                os.unlink(pdf_path)

            # st.success("PDF has been successfully loaded!")
            return True

        except Exception as e:
            st.error(f"Error: {str(e)}")
            return False
    return True

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Auto-load PDF from same folder instead of asking for upload
default_pdf_path = "SatyuktQueries.pdf"  # Change this filename to your actual PDF
if os.path.exists(default_pdf_path):
    class DummyFile:
        def read(self):
            with open(default_pdf_path, "rb") as f:
                return f.read()
    pdf_input_from_user = DummyFile()

    if initialize_vector_db(pdf_input_from_user):
        st.success("Hi there! 👋 How can I assist you today? Feel free to ask me anything About Us — I’m here to help You!")
else:
    st.error(f"PDF file '{default_pdf_path}' not found in the project directory.")

# Chat interface
if "vector_store" in st.session_state:
    st.subheader("Chat History")
    for msg in st.session_state.chat_history:
        role = "**You:**" if msg["role"] == "user" else "**Bot:**"
        st.write(f"{role} {msg['content']}")
        st.write("---")

    user_prompt = st.text_input("Enter your question in your language:")

    if st.button("Send Message"):
        if user_prompt:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})

            with st.spinner("Getting answer..."):
                document_chain = create_stuff_documents_chain(llm, prompt)
                retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 5})
                retrieval_chain = create_retrieval_chain(retriever, document_chain)

                response = retrieval_chain.invoke({'input': user_prompt})
                answer = response['answer']

                if is_out_of_context(answer):
                    answer = "Let me connect you with the right team for this! Drop a message to support@satyukt.com — they’ll take it from here. 🙌"

                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.experimental_rerun()
        else:
            st.error("Please enter a question.")
else:
    st.info("Waiting for Our Virtual Assistant...")
