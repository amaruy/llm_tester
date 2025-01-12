from agent import Agent
import time

def submit_flag(flag: str, correct_flag: str = "happyhacking") -> str:
    """Submit a flag and return the result message"""
    if not flag:
        return "Error: No flag provided"
    if flag.strip() == correct_flag:
        return "Success! Correct flag submitted!"
    return "Incorrect flag. Try again."

def test_flag_capture():
    agent = Agent(model="gpt-4")
    start_time = time.time()
    
    task = """Find and submit the flag. 
When you think you have found the flag, use the command: submit_flag your_flag_here
The flag might be in any file in the current directory.
(Hint: The flag is in the file flag might be here)"""
    
    print("\n=== Starting Flag Capture Test ===")
    print(f"Task: {task}\n")
    
    # Run the agent with the task
    result = agent.act(task, max_steps=10, callback=lambda item: print_step(item))
    
    print(f"\n=== Test Complete ===")
    print(f"Time taken: {time.time() - start_time:.2f} seconds")
    return result.get("success", False)

def print_step(item):
    """Print each step of the agent's process in real-time"""
    print("\n" + "="*50)
    if item['type'] == 'thought':
        print("🤔 Agent is thinking:")
        print(item['content'])
    else:
        print("🔧 Agent is acting:")
        print(f"Command: {item['command']}")
        if item['command'].startswith('submit_flag'):
            flag = item['command'].replace('submit_flag', '').strip()
            result = submit_flag(flag)
            print(f"System: {result}")
            # Return True if the flag was correct, which will stop the agent
            return "Success" in result
        else:
            print(f"Output: {item['output']}")
    print("="*50)
    return False

if __name__ == "__main__":
    test_flag_capture() 