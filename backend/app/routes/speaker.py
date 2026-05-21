from fastapi import APIRouter, Depends

from app.models.schema import VoiceTrainRequest
from app.services.auth import get_current_user_id
from app.services.gemini_embedding import get_embedding
from app.services.speaker_training import add_voice, get_voice_profiles

router = APIRouter(tags=["speaker"])


@router.post("/train")
def train_voice(payload: VoiceTrainRequest, _user_id: str = Depends(get_current_user_id)):
    sample = payload.sample_text or payload.name
    embedding = get_embedding(sample)
    add_voice(payload.name, embedding)
    return {"msg": "voice profile saved", "name": payload.name}


@router.get("/profiles")
def list_profiles(_user_id: str = Depends(get_current_user_id)):
    return {"profiles": get_voice_profiles()}
