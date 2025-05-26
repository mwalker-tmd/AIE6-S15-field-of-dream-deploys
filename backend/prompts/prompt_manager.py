from .base_prompts import InstructionPrompt, QueryPrompt

class PromptManager:
    def __init__(self):
        self.instruction_prompt = InstructionPrompt(
            "Use the following context to answer a user's question. If you don't know, say so."
        )
        self.query_prompt = QueryPrompt(
            "Context:\n{context}\n\nQuestion:\n{question}"
        )

    def create_messages(self, question: str, context: str):
        """Create system and user messages for the chat"""
        return [
            self.instruction_prompt.create_message(),
            self.query_prompt.create_message(question=question, context=context)
        ] 