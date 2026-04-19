from fastapi import FastAPI
from pydantic import BaseModel
from llm import analyze_incident_with_llm
from memory import store_incident, retrieve_similar_incidents
from utils import predict_future_failures

app = FastAPI(title="Predictive Incident Intelligence Agent")

class LogRequest(BaseModel):
    log: str

class AnalysisResponse(BaseModel):
    analysis: str
    prediction: str
    memory_used: bool

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_endpoint(request: LogRequest):
    # Handle empty input
    if not request.log or not request.log.strip():
        return AnalysisResponse(
            analysis="Error: Empty input log provided. Please provide a valid log.",
            prediction="None",
            memory_used=False
        )
    
    log = request.log.strip()
    
    # 1. Retrieve from memory
    context = retrieve_similar_incidents(log)
    memory_used = bool(context)
    
    # 2. Analyze with LLM
    analysis = analyze_incident_with_llm(log, context)
    
    # 3. Predict future failures
    prediction = predict_future_failures(log)
    
    # 4. Store the new incident in memory (only if analysis didn't error out)
    if "Error" not in analysis:
        store_incident(log, analysis)
        
    return AnalysisResponse(
        analysis=analysis,
        prediction=prediction,
        memory_used=memory_used
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
