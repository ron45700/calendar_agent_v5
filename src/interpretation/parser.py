from src.config import settings

def parse(raw: str) -> dict:
    parts = raw.split()    
    return {"first": parts[0], "count": len(parts) , "who will reply": settings.REPLY_PREFIX}

