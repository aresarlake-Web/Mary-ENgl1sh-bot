"""
Static quiz question bank used by the quiz service.
"""

from typing import TypedDict


class QuizItem(TypedDict):
    question: str
    answer: str
    explanation: str


QUIZ_BANK: list[QuizItem] = [
    {
        "question": "Fill in the blank: She ___ to school every day.\na) go\nb) goes\nc) going",
        "answer": "b",
        "explanation": "'goes' is correct because with he/she/it we add -s to the verb in Present Simple.",
    },
    {
        "question": "Which sentence is correct?\na) I have seen him yesterday\nb) I saw him yesterday\nc) I did see him yesterday",
        "answer": "b",
        "explanation": "'I saw him yesterday' is correct. We use Past Simple (not Present Perfect) with specific past time expressions like 'yesterday'.",
    },
    {
        "question": "Fill in the blank: If I ___ rich, I would travel the world.\na) am\nb) was\nc) were",
        "answer": "c",
        "explanation": "'were' is correct. In Second Conditional (unreal situations), we use 'were' for all persons.",
    },
    {
        "question": "Choose the correct word: The news ___ surprising.\na) are\nb) is\nc) were",
        "answer": "b",
        "explanation": "'is' is correct. 'News' looks plural but is an uncountable noun — always singular!",
    },
    {
        "question": "Fill in the blank: I'm looking forward ___ you.\na) to see\nb) seeing\nc) to seeing",
        "answer": "c",
        "explanation": "'to seeing' is correct. 'Look forward to' is always followed by a gerund (-ing form).",
    },
    {
        "question": "Which is correct?\na) He doesn't knows\nb) He don't know\nc) He doesn't know",
        "answer": "c",
        "explanation": "'doesn't know' is correct. With he/she/it, use 'doesn't' + base verb (no -s on the main verb).",
    },
    {
        "question": "Fill in the blank: This is the best movie ___ I've ever seen.\na) what\nb) which\nc) that",
        "answer": "c",
        "explanation": "'that' is correct. After superlatives (best, worst, etc.) we use 'that', not 'which'.",
    },
    {
        "question": "Choose the right tense: By 2030, scientists ___ a cure.\na) will find\nb) will have found\nc) found",
        "answer": "b",
        "explanation": "'will have found' is correct — Future Perfect is used for actions completed before a future point in time.",
    },
]
