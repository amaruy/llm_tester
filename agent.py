import logging
from datetime import datetime
import os
import litellm
from typing import List, Dict

class Agent:
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.conversation_history: List[Dict] = []
        
        # Disable LiteLLM verbose logging
        litellm.set_verbose = False
        logging.getLogger("litellm").setLevel(logging.ERROR)
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs/agent', exist_ok=True)
        
        # Setup agent-specific logging with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'logs/agent/agent_{timestamp}.log'
        
        # Configure agent logger
        self.logger = logging.getLogger("agent")
        self.logger.setLevel(logging.INFO)
        
        # Remove any existing handlers
        self.logger.handlers = []
        
        # Add file handler
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        self.logger.info(f"Agent initialized with model: {model}")

    def think(self, task: str, system_prompt: str, last_output: str = None) -> str:
        """Generate thoughts about how to approach the task"""
        self.logger.info(f"Thinking about task: {task}")
        self.logger.debug(f"System prompt: {system_prompt}")
        if last_output:
            self.logger.debug(f"Last output: {last_output}")
        
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
        self.logger.info(f"Generated thought: {thought[:100]}...")  # Log first 100 chars of thought
        return thought

    def get_next_command(self, thought: str, task: str, system_prompt: str, last_output: str = None) -> str:
        """Get the next command based on the thought and previous output"""
        self.logger.info("Generating next command")
        self.logger.debug(f"Based on thought: {thought[:100]}...")
        
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
        self.logger.info(f"Generated command: {response.choices[0].message.content.strip()}")
        return response.choices[0].message.content.strip()