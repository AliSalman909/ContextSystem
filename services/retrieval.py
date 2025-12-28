from ..settings import settings
from .pinecone_client import index as pinecone_index
from .embeddings import embed_text


def retrieve_customer_context(customer_id: str, top_k: int = 12) -> list[dict]:
    """
    Queries Pinecone for chunks relevant to building a questionnaire for this customer.
    Returns list of metadata dicts.
    """
    query_text = (
        "Extract unclear requirements, missing technical details, constraints, integrations, "
        "non-functional requirements, acceptance criteria, data sources, security, roles."
    )
    qvec = embed_text(query_text)

    res = pinecone_index.query(
        vector=qvec,
        top_k=top_k,
        include_metadata=True,
        namespace=settings.PINECONE_NAMESPACE,
        filter={"customer_id": {"$eq": customer_id}},
    )

    matches = res.get("matches", []) if isinstance(res, dict) else getattr(res, "matches", [])
    out = []
    for m in matches:
        md = m.get("metadata", {}) if isinstance(m, dict) else m.metadata
        if md:
            out.append(md)
    return out
