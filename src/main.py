import time
from src.utils import listen, speak
from src.command_handler import handle_command

def main():
    speak("Jarvis here! What we working on today sir?")
    
    running = True
    while running:
        command = listen()
        if command:
            running = handle_command(command)
        
        # Small delay to prevent CPU hogging if listen returns immediately
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping...")
