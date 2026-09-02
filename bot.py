import os
import time
from dotenv import load_dotenv
import telebot
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")

if not TELEGRAM_BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN is not set in the .env file.")
    exit(1)

print("Initializing bot...")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

print("Loading document...")
loader = TextLoader("data/knowledge_base.txt", encoding="utf-8")
documents = loader.load()

print("Splitting document into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

print("Initializing embeddings (this might take a moment to download the model the first time)...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("Creating local vector database...")
vectorstore = FAISS.from_documents(docs, embeddings)

print("Setting up LLM via LM Studio...")
# Connects to LM Studio's OpenAI compatible API
llm = ChatOpenAI(
    base_url=LM_STUDIO_URL,
    api_key="not-needed",
    temperature=0.3,
    # The model name here doesn't matter much as LM Studio routes to whichever model is loaded
    model="local-model" 
)

# Custom prompt template to constrain the LLM to only answer based on context
template = """You are a helpful and friendly AI assistant for Magic Island Robotics (FRC 5800).
You can answer any questions the user asks. If the user asks about the team, use the provided context below to inform your answer. For all other topics, feel free to use your general knowledge and have a normal conversation.
Keep your answers natural and engaging. Answer in the same language the user asked (usually Portuguese or English).

Context about the team (use only if relevant to the question):
{context}

Question: {question}

Answer:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

print("Creating RAG chain...")
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Eu sou o assistente IA da Magic Island Robotics (FRC 5800). Me pergunte algo sobre nosso Outreach Report 2026!")

@bot.message_handler(func=lambda message: True)
def answer_question(message):
    question = message.text
    chat_id = message.chat.id
    
    # Check if the bot was tagged
    if not question or "@magicalliancebot" not in question:
        return
    
    # Send a typing indicator
    bot.send_chat_action(chat_id, 'typing')
    
    try:
        # Limpa a tag da pergunta para não confundir a IA
        clean_question = question.replace("@magicalliancebot", "").strip()
        print(f"Received question: {clean_question}")
        
        # Se a pergunta ficou vazia após remover a tag, não faz nada
        if not clean_question:
            bot.reply_to(message, "Por favor, faça uma pergunta após me marcar!")
            return
            
        result = qa_chain.invoke({"query": clean_question})
        answer = result.get("result", "").strip()
        
        # Evita o erro 400 do Telegram se a IA retornar um texto vazio
        if not answer:
            answer = "Desculpe, o modelo de IA gerou uma resposta vazia. Isso pode acontecer dependendo do modelo carregado no LM Studio."
            
        bot.reply_to(message, answer)
    except Exception as e:
        print(f"Error processing question: {e}")
        bot.reply_to(message, "Desculpe, ocorreu um erro ao processar sua pergunta. Verifique se o servidor do LM Studio está rodando e se há um modelo carregado.")

if __name__ == "__main__":
    print("Bot is running and listening for messages! Press Ctrl+C to stop.")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(5)
