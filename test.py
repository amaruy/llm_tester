import logging
import os
from abc import ABC, abstractmethod
from agent import Agent
from datetime import datetime

class BaseTest(ABC):
    def __init__(self, name: str, verbosity: str = "INFO"):
        self.name = name
        self.start_time = None
        self.interaction_count = 0
        self.setup_logging(verbosity)
        
    def setup_logging(self, verbosity: str):
        """Setup test-specific logging"""
        # Create logs directory
        os.makedirs(f'logs/tests/{self.name}', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'logs/tests/{self.name}/test_{timestamp}.log'
        
        self.logger = logging.getLogger(f"test.{self.name}")
        self.logger.setLevel(getattr(logging, verbosity.upper()))
        
        # Remove any existing handlers
        self.logger.handlers = []
        
        # File handler for detailed logging
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler for basic output
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def run_test(self, agent: Agent) -> bool:
        """Run the test with the specified agent"""
        self.start_time = datetime.now()
        self.logger.info(f"=== Starting {self.name} Test ===")
        self.logger.info(f"Start time: {self.start_time}")
        
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
            
            self.interaction_count += 1
            
            if is_finished:
                end_time = datetime.now()
                duration = end_time - self.start_time
                self.logger.info("✅ Test completed successfully!")
                self.logger.info(f"Test duration: {duration}")
                self.logger.info(f"Total interactions: {self.interaction_count}")
                return True
                
            steps += 1
            
        end_time = datetime.now()
        duration = end_time - self.start_time
        self.logger.info("❌ Test failed - max steps reached")
        self.logger.info(f"Test duration: {duration}")
        self.logger.info(f"Total interactions: {self.interaction_count}")
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