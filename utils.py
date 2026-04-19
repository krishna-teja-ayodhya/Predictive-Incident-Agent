def predict_future_failures(log: str) -> str:
    """
    Predict possible future failures based on simple but meaningful log heuristics.
    """
    log_lower = log.lower()
    predictions = []
    
    if "memory" in log_lower or "oom" in log_lower or "heap space" in log_lower:
        predictions.append("High risk of Out of Memory (OOM) cascade. Other services sharing this node might be killed soon.")
        
    if "cpu" in log_lower or "load" in log_lower or "timeout" in log_lower:
        predictions.append("Potential deadlock or CPU throttling detected. Expect dependent services to start timing out.")
        
    if "disk" in log_lower or "space" in log_lower or "storage" in log_lower:
        predictions.append("Disk exhaustion imminent. Logs will stop writing, and database transactions may fail entirely.")
        
    if "connection refused" in log_lower or "network" in log_lower or "dns" in log_lower:
        predictions.append("Network partition detected. Downstream APIs will likely begin returning 502/503 errors.")
        
    if not predictions:
        predictions.append("No immediate cascading failures predicted based on known heuristics, but continue monitoring.")
        
    return " | ".join(predictions)
