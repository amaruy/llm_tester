import logging
import litellm
from typing import List, Dict

class Agent:
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.conversation_history: List[Dict] = []
        self.logger = logging.getLogger("agent")

    def think(self, task: str, system_prompt: str, last_output: str = None) -> str:
        """Generate thoughts about how to approach the task"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Task: {task}"}
        ]
        
        if last_output:
            messages.append({"role": "user", "content": f"Last output:\n{last_output}"})
        
        messages.extend(self.conversation_history[-3:])
        
        response = litellm.completion(
            model=self.model,
            messages=messages,
            max_tokens=200
        )
        
        thought = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": thought})
        return thought

    def get_next_command(self, thought: str, task: str, system_prompt: str, last_output: str = None) -> str:
        """Get the next command based on the thought and previous output"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Previous thought: {thought}\nTask: {task}"}
        ]
        
        if last_output:
            messages.append({"role": "user", "content": f"Previous output:\n{last_output}"})
        
        response = litellm.completion(
            model=self.model,
            messages=messages,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()