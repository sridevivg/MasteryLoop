"""
Socratic AI Tutor Service for MasteryLoop.
Implements 6 pedagogical modes (HINT, TEACH_FROM_BASICS, DEBUG, INTERVIEW, QUICK_REVISION, EXAM_MODE),
multilingual responses (English, Tamil, Tanglish), RAG grounding via Qdrant,
and adaptive personalization based on learner mastery and prerequisite graphs.
"""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.schemas.tutor import TutorMode, TutorLanguage, SourceCitation, TutorChatResponse
from app.models.user import User
from app.models.curriculum import Skill
from app.models.mastery import LearnerSkillMastery
from app.agentic.rag import vector_store
from app.services.skill_graph import SkillDependencyGraph

logger = logging.getLogger(__name__)


class SocraticTutorEngine:
    """Orchestrates RAG retrieval, pedagogical mode formatting, and multilingual tutoring."""

    @staticmethod
    def generate_response(
        message: str,
        mode: TutorMode,
        language: TutorLanguage,
        user: User,
        skill_id: Optional[str],
        db: Session,
        history: Optional[List[Dict[str, str]]] = None
    ) -> TutorChatResponse:
        # 1. Retrieve Learner's Personal Mastery Profile & Prerequisite Context
        mastery_est = 0.50
        prereq_gaps = []
        target_skill = None

        if skill_id:
            target_skill = db.query(Skill).filter((Skill.id == skill_id) | (Skill.code == skill_id)).first()
            if target_skill:
                mastery_record = db.query(LearnerSkillMastery).filter(
                    LearnerSkillMastery.user_id == user.id,
                    LearnerSkillMastery.skill_id == target_skill.id
                ).first()
                if mastery_record:
                    mastery_est = mastery_record.estimate

                # Check prerequisite foundations
                graph = SkillDependencyGraph.from_db(db)
                mastered_ids = {
                    m.skill_id for m in db.query(LearnerSkillMastery)
                    .filter(LearnerSkillMastery.user_id == user.id, LearnerSkillMastery.estimate >= 0.70).all()
                }
                missing_foundations = graph.get_unmastered_foundations(target_skill.id, mastered_ids)
                prereq_gaps = [graph.skills_by_id[fid].name for fid in missing_foundations if fid in graph.skills_by_id]

        # 2. RAG Semantic Search in Qdrant
        search_query = f"{message} {target_skill.name if target_skill else ''}"
        retrieved_chunks = vector_store.search(
            query=search_query,
            skill_id=target_skill.id if target_skill else None,
            top_k=3,
            min_score=0.18
        )
        if not retrieved_chunks:
            # Fall back to unconstrained semantic retrieval
            retrieved_chunks = vector_store.search(
                query=search_query,
                top_k=3,
                min_score=0.18
            )

        citations: List[SourceCitation] = []
        context_texts = []
        for chunk in retrieved_chunks:
            citations.append(SourceCitation(
                title=chunk["title"],
                chunk_text=chunk["content"][:200] + "...",
                relevance_score=chunk["score"],
                domain=chunk.get("domain")
            ))
            context_texts.append(chunk["content"])

        combined_context = "\n\n".join(context_texts) if context_texts else ""

        # 3. Generate Grounded Socratic Response based on Mode & Language
        from app.agentic.llm_client import get_llm_provider
        llm_provider = get_llm_provider()
        system_prompt = (
            f"You are the MasteryLoop Socratic Placement AI Tutor operating in mode: {mode.value}.\n"
            f"Target Skill: {target_skill.name if target_skill else 'General Engineering Foundations'}.\n"
            f"Learner Mastery Level: {mastery_est:.2f}.\n"
            f"Prerequisite Gaps: {', '.join(prereq_gaps) if prereq_gaps else 'None detected'}.\n"
            f"Target Language: {language.value}.\n"
            f"CRITICAL PEDAGOGICAL RULES:\n"
            f"- Ground response strictly in the retrieved curriculum context below.\n"
            f"- {'UNDER NO CIRCUMSTANCES reveal answer keys or complete worked solutions in EXAM mode.' if mode in (TutorMode.EXAM, TutorMode.EXAM_MODE) else 'Encourage first-principles derivation.'}\n\n"
            f"Retrieved Curriculum Context:\n{combined_context}"
        )
        llm_result = llm_provider.generate_tutor_response(
            system_prompt=system_prompt,
            user_prompt=message
        )

        provider_used = llm_result["provider_used"]
        if llm_result.get("text"):
            response_text = llm_result["text"]
            suggestions = ["Can you elaborate further?", "Give me a practice problem on this.", "Explain another approach."]
        else:
            response_text, suggestions = SocraticTutorEngine._format_mode_response(
                message=message,
                mode=mode,
                language=language,
                skill=target_skill,
                mastery=mastery_est,
                prereq_gaps=prereq_gaps,
                context=combined_context,
                citations_count=len(citations)
            )

        return TutorChatResponse(
            response=response_text,
            mode=mode,
            language=language,
            citations=citations,
            followup_suggestions=suggestions,
            provider_used=provider_used
        )

    @staticmethod
    def _format_mode_response(
        message: str,
        mode: TutorMode,
        language: TutorLanguage,
        skill: Optional[Skill],
        mastery: float,
        prereq_gaps: List[str],
        context: str,
        citations_count: int
    ) -> (str, List[str]):
        """Generates pedagogical mode responses with verified curriculum facts."""
        skill_name = skill.name if skill else "this placement topic"

        # Adaptive prerequisite advisory
        foundation_note = ""
        if prereq_gaps:
            foundation_note = f"\n\n*(Adaptive Note: I notice your foundations in {', '.join(prereq_gaps[:2])} are developing. Mastering those will make {skill_name} much easier!)*"

        # 1. HINT MODE (Progressive hints, never reveal raw answer key)
        if mode == TutorMode.HINT:
            if language == TutorLanguage.TAMIL:
                text = (
                    f"**குறிப்பு 1 (கருத்து நிலை):** {skill_name} சிக்கலுக்கு, முதலில் உள்ளீட்டின் பண்புகளைப் பாருங்கள் (வரிசைப்படுத்தப்பட்டுள்ளதா அல்லது இல்லையா?).\n"
                    f"**குறிப்பு 2 (அணுகுமுறை):** {context[:180] if context else 'இரு சுட்டிகள் அல்லது ஹேஷிங் உத்திகளைப் பயன்படுத்துங்கள்.'}\n"
                    f"இப்போது இந்த உத்தியை வைத்து உங்கள் அடுத்த படியை முயற்சிக்கவும்!"
                )
            elif language == TutorLanguage.TANGLISH:
                text = (
                    f"**Hint 1 (Conceptual):** {skill_name}-ku first input data-va observe பண்ணுங்க. Sorted-ah illana unsorted-ah?\n"
                    f"**Hint 2 (Approach):** {context[:180] if context else 'Two pointers use pannalama illa hash table thevaiya nu yosinga.'}\n"
                    f"Full answer-ah naan reveal panna maaten — indha hint-ah base panni attempt pannunga!"
                )
            else:
                text = (
                    f"**Hint 1 (Structural Clue):** Notice the invariant constraints in {skill_name}. Ask yourself: What property of the input remains constant as we iterate?\n\n"
                    f"**Hint 2 (Algorithmic Direction):** {context[:220] if context else 'Consider if a two-pointer scan or state tracking reduces the time complexity from O(N^2) to O(N).'}\n\n"
                    f"Take a moment to work through this step before requesting a direct solution."
                )
            suggestions = ["Can you give me a more specific hint?", "How does this compare to brute force?", "Show me a small example."]

        # 2. TEACH FROM BASICS
        elif mode == TutorMode.TEACH_FROM_BASICS:
            if language == TutorLanguage.TAMIL:
                text = (
                    f"### {skill_name}: அடிப்படைக் கருத்து விளக்கம்\n\n"
                    f"வாருங்கள், ஆரம்பத்தில் இருந்து எளிமையாகப் புரிந்துகொள்வோம்.\n\n"
                    f"**1. முக்கிய கொள்கை:** {context if context else 'இந்த கருத்து சிக்கலான கணக்குகளை எளிமைப்படுத்துகிறது.'}\n\n"
                    f"**2. ஏன் இது முக்கியம்?** நேர்காணல்களில் கணினி வளங்களை (Time & Space) சிக்கனப்படுத்துவதை சோதிக்க இது கேட்கப்படுகிறது."
                    f"{foundation_note}"
                )
            elif language == TutorLanguage.TANGLISH:
                text = (
                    f"### {skill_name}: Basics-la irundhu step-by-step padikalam!\n\n"
                    f"**Step 1 - The Core Idea:**\n{context if context else 'Indha algorithm/concept namma complexity-ah dramatically reduce pannum.'}\n\n"
                    f"**Step 2 - Real-World Intuition:**\nIterate pannum podhu unwanted calculations-ah avoid pandradhu dhaan idhoda main objective."
                    f"{foundation_note}"
                )
            else:
                text = (
                    f"### Understanding {skill_name} from First Principles\n\n"
                    f"Let's break this down into clear, digestible steps without skipping essential foundations:\n\n"
                    f"**1. The Fundamental Concept:**\n{context if context else 'This technique transforms brute-force complexity into efficient linear or logarithmic execution.'}\n\n"
                    f"**2. Why It Works:**\nBy leveraging monotonic properties and eliminating redundant computations, each step makes verifiable progress toward the goal."
                    f"{foundation_note}"
                )
            suggestions = ["Can you walk through a step-by-step code example?", "What are the common edge cases?", "Test me on this concept."]

        # 3. DEBUG MODE
        elif mode == TutorMode.DEBUG:
            if language == TutorLanguage.TANGLISH:
                text = (
                    f"### Debugging Assistant for {skill_name}\n\n"
                    f"Unge code-la common-ah vara 3 critical bugs idhu dhaan:\n"
                    f"1. **Boundary & Off-by-One Conditions:** Loop termination index correct-ah check pannunga (e.g. `<= len(nums) - 1`).\n"
                    f"2. **State Mutation:** Reference copy pannama independent state maintain pannunga.\n"
                    f"3. **Edge Case Coverage:** Empty input `[]` or single element `[x]` pass aagudha nu verify pannunga."
                )
            else:
                text = (
                    f"### Systematic Debugging Guide for {skill_name}\n\n"
                    f"To isolate the root cause of the error in your implementation:\n\n"
                    f"1. **Check Base Cases & Boundaries:** Ensure loop indices and recursion base cases do not exceed array bounds or cause infinite recursion.\n"
                    f"2. **Trace State Transitions:** Verify that variables update as intended at every iteration.\n"
                    f"3. **Inspect Edge Cases:** Test against minimum length arrays, duplicate elements, and negative values.\n\n"
                    f"**Curriculum Reference Insight:**\n{context[:200] if context else 'Examine space complexity overhead and off-by-one pointer mutations.'}"
                )
            suggestions = ["How do I fix the index out of bounds error?", "Is there a memory leak here?", "Analyze the time complexity."]

        # 4. INTERVIEW MODE
        elif mode == TutorMode.INTERVIEW:
            text = (
                f"### Placement Technical Interview Simulation\n\n"
                f"**Interviewer Question:**\n"
                f"*\"Could you explain how you would optimize a solution for {skill_name}? "
                f"Specifically, walk me through your time and space complexity trade-offs, and state what edge cases you would check before shipping to production.\"*\n\n"
                f"**Evaluation Criteria:**\n"
                f"- Clear communication of algorithmic invariants.\n"
                f"- Accurate Big-O analysis ($O(N)$ vs $O(N^2)$).\n"
                f"- Identification of boundary conditions.\n\n"
                f"Please provide your response as you would in a live placement interview."
            )
            suggestions = ["Here is my approach...", "What is the follow-up question?", "Rate my explanation."]

        # 5. QUICK REVISION
        elif mode == TutorMode.QUICK_REVISION:
            text = (
                f"### Quick Revision Cheat-Sheet: {skill_name}\n\n"
                f"**Key Takeaways:**\n"
                f"- **Core Invariant:** {context[:180] if context else 'Monotonic state traversal and linear reduction.'}\n"
                f"- **Optimal Complexity:** Time: $O(N)$, Space: $O(1)$ auxiliary.\n"
                f"- **Frequent Pitfall:** Forgetting to handle unsorted inputs or empty arrays.\n"
                f"- **Interview Keyword Checklist:** Invariants, Two Pointers, Paging, ACID, Normalized Keys."
            )
            suggestions = ["Give me a 2-minute recap of the next topic.", "What formulas must I memorize?", "Give me a practice question."]

        # 6. EXAM MODE (Zero Answer Key Leakage)
        elif mode in (TutorMode.EXAM, TutorMode.EXAM_MODE):
            text = (
                f"### Exam Mode Practice Scenario: {skill_name}\n\n"
                f"**Practice Challenge:**\n"
                f"Analyze the following problem under timed assessment conditions:\n\n"
                f"> Explain the worst-case behavior and design an optimal algorithm for {skill_name}.\n\n"
                f"*(Note: In Exam Mode, exact answer keys and complete worked solutions are restricted until you submit your complete attempt.)*\n\n"
                f"Formulate your complete answer below."
            )
            suggestions = ["Submit my exam attempt", "Give me another practice question", "Exit exam mode"]

        else:
            text = f"Here is curriculum-grounded guidance on {skill_name}:\n\n{context}"
            suggestions = ["Tell me more", "Give an example"]

        return (text, suggestions)


tutor_service = SocraticTutorEngine()
