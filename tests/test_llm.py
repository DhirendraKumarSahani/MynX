from app.models.llm_model import LLMService
from langchain_core.messages import HumanMessage

def test_llm():
    llm_service = LLMService()

    response = llm_service.invoke([
        HumanMessage(content="Explain machine learning in one sentence")
    ])

    print("\n LLM Response : \n")
    print(response.content)

if __name__ == "__main__":
    test_llm()