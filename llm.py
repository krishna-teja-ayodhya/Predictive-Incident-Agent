import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_incident_with_llm(log: str, context: str = "") -> str:
    """Analyze the incident using Groq API."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY is not set. Please add it to your .env file."
    
    try:
        client = Groq(api_key=api_key)
        
        prompt = f"Analyze the following system log and provide the root cause and a solution.\n\nLog:\n{log}\n"
        if context:
            prompt += f"\nContext from similar past incidents (use this to improve your response):\n{context}\n"
            
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior DevOps and SRE engineer. Analyze system logs to find root causes and suggest practical solutions. Keep your response clear, structured, and concise."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error analyzing incident with Groq API: {str(e)}"
