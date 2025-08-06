
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

PROMPT_TEMPLATE_1 = """
As a chat assistant, you will provide details on how to perform task base on the context:

{context}

---

Answer the question and provide a step-by-step guide on how to perform the task.
Avoid  using the the sentence "Base on the context or document" in your response.
{question}
"""