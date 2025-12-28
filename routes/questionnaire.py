from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models
from ..services.questionnaire_gen import generate_questionnaire

router = APIRouter()


@router.post("/{customer_id}/questionnaire/generate")
def generate(customer_id: str, db: Session = Depends(get_db)):
    try:
        data = generate_questionnaire(customer_id=customer_id)

        # 1) Create Questionnaire record
        qn = models.Questionnaire(
            customer_id=customer_id,
            title=data.get("title") or "Requirements Clarification Questionnaire",
            status="draft",
        )
        db.add(qn)
        db.commit()
        db.refresh(qn)

        # 2) Create Question records
        for sec in data.get("sections", []):
            topic_default = sec.get("title")
            for item in sec.get("questions", []):
                db.add(models.Question(
                    questionnaire_id=qn.id,
                    text=item.get("q", ""),
                    answer=None,
                    priority=item.get("priority"),
                    topic_category=item.get("topic_category") or topic_default,
                    source_chunk_id=item.get("source_chunk_id"),  # optional; usually None for MVP
                ))
        db.commit()

        # 3) Return
        return {"questionnaire_id": qn.id, "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
