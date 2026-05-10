question_prompt_template = """
You are an expert at creating 10 questions based on given materials and documentation.
Your goal is to prepare a student for their exam by generating 10 questions.
You do this by asking questions about the text below:

------------
{text}
------------

Create questions that will prepare the students for their exams.
Make sure not to loose any important information.
Respond with only questions. No other information.

QUESTIONS:
"""

refine_question_template = """
You are an expert at creating 10 questions based on materials and documentation.
Your goal is to help a student to prepare for their exam by generating 10 questions.
We have recieved some questions to a certain extent : 
{existing_answer}

We have the option to refine the existing questions or add the new ones deleting unrelevant ones (only if necessary) with some more context below.

------------
{text}
------------

Given the new context, refine the original questions in English.
If the context is not helpful, please provided the original question.
Respond with only 10 questions. No other information.

QUESTIONS:
"""

retrieval_promt = """Answer the question based only on the context below:

{context}

Question: {question}
"""