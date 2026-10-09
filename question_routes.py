from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import (
    load_documents,
    retrieve_relevant_chunks
)

from app.services.generation_service import (
    generate_answer,
    generate_general_answer
)

from app.services.evidence_service import (
    calculate_confidence,
    get_confidence_label
)

from app.services.misconception_service import (
    detect_misconception
)

from app.services.conflict_service import (
    detect_source_conflict
)

from app.services.freshness_service import (
    check_source_freshness
)

from app.utils.citation_formatter import (
    format_sources
)


router = APIRouter(
    prefix="/question",
    tags=["Question"]
)


class QuestionRequest(BaseModel):
    question: str


@router.post("/")
def ask_question(
    request: QuestionRequest
):

    documents = load_documents()

    relevant_documents = retrieve_relevant_chunks(
        documents,
        request.question
    )

    confidence = calculate_confidence(
        request.question,
        relevant_documents
    )

    print(
        "QUESTION:",
        request.question
    )

    print(
        "RETRIEVED CHUNKS:",
        len(relevant_documents)
    )

    print(
        "CONFIDENCE:",
        confidence
    )


    # ---------------------------------
    # SOURCE CONFLICT
    # ---------------------------------

    conflict_result = detect_source_conflict(
        relevant_documents
    )


    # ---------------------------------
    # SOURCE FRESHNESS
    # ---------------------------------

    freshness_result = check_source_freshness(
        relevant_documents
    )


    # ---------------------------------
    # SOURCE-GROUNDED ANSWER
    # ---------------------------------

    if (
        relevant_documents
        and confidence >= 50
    ):

        context = "\n\n".join(
            document["content"]
            for document in relevant_documents
        )

        result = generate_answer(
            request.question,
            context
        )


        if result.get(
            "error"
        ) == "quota_exceeded":

            return {
                "question": request.question,
                "answer": result["answer"],
                "sources": [],
                "confidence": 0,
                "confidence_level": "Unavailable",
                "misconception_check": "Not available",
                "conflict_check": conflict_result,
                "freshness_check": freshness_result,
                "answer_mode": "AI Service Unavailable"
            }


        misconception = detect_misconception(
            request.question,
            context
        )


        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": format_sources(
                relevant_documents
            ),
            "confidence": confidence,
            "confidence_level": get_confidence_label(
                confidence
            ),
            "misconception_check": misconception,
            "conflict_check": conflict_result,
            "freshness_check": freshness_result,
            "answer_mode": "Source-Grounded",
            "provider": result.get(
                "provider",
                "Gemini"
            )
        }


    # ---------------------------------
    # GENERAL ANSWER
    # ---------------------------------

    result = generate_general_answer(
        request.question
    )


    if result.get(
        "error"
    ) == "quota_exceeded":

        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": [],
            "confidence": 0,
            "confidence_level": "Unavailable",
            "misconception_check": "Not available",
            "conflict_check": conflict_result,
            "freshness_check": freshness_result,
            "answer_mode": "AI Service Unavailable"
        }


    return {
        "question": request.question,
        "answer": result.get(
            "answer",
            "No answer available."
        ),
        "sources": result.get(
            "sources",
            []
        ),
        "confidence": 0,
        "confidence_level": "Low",
        "misconception_check": "Not available",
        "conflict_check": conflict_result,
        "freshness_check": freshness_result,
        "answer_mode": "General Academic",
        "provider": result.get(
            "provider",
            "Gemini"
        )
    }