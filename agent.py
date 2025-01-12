import os
import subprocess
import datetime
import json
import litellm
from typing import List, Dict
import logging

class Agent:
    def __init__(self, model: str = "gpt-4", log_dir: str = "logs"):
        """Initialize the agent with a specific model and logging directory"""
        self.model = model
        self.conversation_history: List[Dict] = []  # Linear history of all interactions
        self.log_dir = log_dir
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Setup logging
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        logging.basicConfig(
            filename=f"{log_dir}/agent_{self.session_id}.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _execute_command(self, command: str) -> str:
        """Execute a shell command and return the output"""
        try:
            self.logger.info(f"Executing command: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout + result.stderr
            
            # Add command and result to conversation history
            self.conversation_history.append({
                "role": "system",
                "content": f"Command executed: {command}\nOutput: {output}"
            })
            
            return output
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out: {command}"
            self.logger.error(error_msg)
            self.conversation_history.append({
                "role": "system",
                "content": f"Error: {error_msg}"
            })
            return error_msg
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            self.logger.error(error_msg)
            self.conversation_history.append({
                "role": "system",
                "content": f"Error: {error_msg}"
            })
            return error_msg

    def think(self, task: str) -> str:
        """Generate thoughts about how to approach the task"""
        try:
            # Construct the prompt using conversation history
            messages = [
                {"role": "system", "content": "You are an agent that can execute shell commands. Think step by step about how to accomplish the given task."},
                {"role": "user", "content": f"Task: {task}"}
            ]
            
            # Add relevant conversation history
            messages.extend(self.conversation_history[-5:])  # Last 5 interactions
            
            response = litellm.completion(
                model=self.model,
                messages=messages,
                max_tokens=500
            )
            
            thought = response.choices[0].message.content
            
            # Add thought to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": thought
            })
            
            self.logger.info(f"Generated thought: {thought}")
            return thought
            
        except Exception as e:
            error_msg = f"Error during thinking: {str(e)}"
            self.logger.error(error_msg)
            return error_msg

    def act(self, task: str, max_steps: int = 5, think_first: bool = True, callback=None) -> Dict:
        """Execute a task through thinking and acting cycles"""
        steps_taken = 0
        results = []
        
        try:
            while steps_taken < max_steps:
                # Think about what to do
                thought = self.think(task) if (think_first or steps_taken > 0) else "Executing initial command..."
                results.append({"type": "thought", "content": thought})
                if callback:
                    callback({"type": "thought", "content": thought})
                
                # Get command from thought
                messages = [
                    {"role": "system", "content": "Based on the thought process, provide a single shell command to execute. Respond with just the command, no explanation."},
                    {"role": "user", "content": f"Previous thought: {thought}\nTask: {task}\n\nCommand to execute:"}
                ]
                
                response = litellm.completion(
                    model=self.model,
                    messages=messages,
                    max_tokens=100
                )
                
                command = response.choices[0].message.content.strip()
                output = self._execute_command(command)
                action_result = {"type": "action", "command": command, "output": output}
                results.append(action_result)
                
                if callback:
                    if callback(action_result):  # If callback returns True, we're done
                        return {"success": True, "results": results}
                
                steps_taken += 1
            
            self._save_session_results(task, results)
            return {"success": False, "results": results}
            
        except Exception as e:
            error_msg = f"Error during task execution: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def _save_session_results(self, task: str, results: List[Dict]):
        """Save the session results to a JSON file"""
        session_data = {
            "session_id": self.session_id,
            "task": task,
            "model": self.model,
            "timestamp": datetime.datetime.now().isoformat(),
            "conversation_history": self.conversation_history,
            "results": results
        }
        
        file_path = f"{self.log_dir}/session_{self.session_id}.json"
        with open(file_path, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        self.logger.info(f"Session results saved to {file_path}") 