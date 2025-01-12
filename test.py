import logging
import os
from abc import ABC, abstractmethod
from agent import Agent

class BaseTest(ABC):
    def __init__(self, name: str, verbosity: str = "INFO"):
        self.name = name
        self.setup_logging(verbosity)
        
    def setup_logging(self, verbosity: str):
        """Setup test-specific logging"""
        self.logger = logging.getLogger(f"test.{self.name}")
        self.logger.setLevel(getattr(logging, verbosity.upper()))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def run_test(self, agent: Agent) -> bool:
        """Run the test with the specified agent"""
        self.logger.info(f"\n=== Starting {self.name} Test ===")
        
        task = self.get_task()
        self.logger.info(f"Task: {task}")
        
        steps = 0
        max_steps = 10
        last_output = None
        
        while steps < max_steps:
            # Think with context
            thought = agent.think(task, self.get_system_prompt(), last_output)
            self.logger.info(f"🤔 Thinking:\n{thought}")
            
            # Act with context
            command = agent.get_next_command(thought, task, self.get_command_prompt(), last_output)
            self.logger.info(f"🔧 Command: {command}")
            
            # Handle command and store output
            output, is_finished = self.handle_command(command)
            self.logger.info(f"Output: {output}")
            last_output = output
            
            if is_finished:
                self.logger.info("✅ Test completed successfully!")
                return True
                
            steps += 1
            
        self.logger.info("❌ Test failed - max steps reached")
        return False

    @abstractmethod
    def handle_command(self, command: str) -> tuple[str, bool]:
        """Handle test-specific commands"""
        pass

    @abstractmethod
    def get_task(self) -> str:
        """Return the task description"""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for thinking"""
        pass

    @abstractmethod
    def get_command_prompt(self) -> str:
        """Return the system prompt for command generation"""
        pass