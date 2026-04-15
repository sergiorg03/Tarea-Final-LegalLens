from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)

def analizar_contrato(texto):
    prompt = f"Analiza este contrato: {texto}"
    return llm.invoke(prompt)