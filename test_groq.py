from src.agent.llm_client import get_llm_response


question = "My office laptop is not connecting to Wi-Fi. What should I do?"


print("\n--- USER QUESTION ---")
print(question)


print("\n--- GROQ AI RESPONSE ---")

answer = get_llm_response(question)

print(answer)