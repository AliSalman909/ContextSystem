from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models, schemas
from ..services.ingest import ingest_document

router = APIRouter()


@router.post("/{customer_id}/documents/upload", response_model=schemas.DocumentOut)
def upload_document(
    customer_id: str,
    doc_type: schemas.DocType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    doc = ingest_document(db=db, customer_id=customer_id, doc_type=doc_type, upload_file=file)
    return doc
