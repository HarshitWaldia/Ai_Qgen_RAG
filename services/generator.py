from langchain_groq import ChatGroq
from core.config import settings
from core.models import GenerateRequest, GeneratedSection, QuestionPaperBlueprint
from core.prompts import qgen_prompt
from services.vector_store import VectorStoreManager
import logging

class PaperGenerator:
    def __init__(self):
        # Bind Pydantic model directly to LLM for guaranteed structural output
        self.llm = ChatGroq(
            model=settings.MODEL_NAME, 
            temperature=0.2, # Low temp for factual consistency
            groq_api_key=settings.GROQ_API_KEY,
            max_tokens=6000
        ).with_structured_output(GeneratedSection)
        self.vstore = VectorStoreManager()

    def generate_paper(self, req: GenerateRequest) -> QuestionPaperBlueprint:
        retriever = self.vstore.get_retriever(req.document_id, k=5)
        
        all_sections =[]
        for sec in req.sections:
            logging.info(f"Generating section: {sec.name}")
            
            # Retrieve relevant context
            query = req.specific_topic if req.specific_topic else f"{sec.q_type} questions about general concepts"
            docs = retriever.invoke(query)
            context = "\n\n".join([d.page_content for d in docs])
            
            if not context.strip():
                raise ValueError("Insufficient context retrieved. Document might be empty.")

            # Generate via RAG + LLM
            chain = qgen_prompt | self.llm
            result: GeneratedSection = chain.invoke({
                "context": context,
                "language": req.language,
                "section_name": sec.name,
                "count": sec.count,
                "q_type": sec.q_type,
                "difficulty": sec.difficulty,
                "marks": sec.marks_per_question
            })
            all_sections.append(result)

        return QuestionPaperBlueprint(
            title="Generated Assessment",
            language=req.language,
            sections=all_sections
        )