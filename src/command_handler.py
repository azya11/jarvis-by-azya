import os
import subprocess
import time
from thefuzz import fuzz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from src.utils import speak
from src.chatgpt import ask_chatgpt

def is_match(command, trigger, threshold=80):
    """
    Checks if the trigger phrase is in the command with fuzzy matching.
    Uses partial_ratio to allow the trigger to be a substring of the command.
    """
    if not command:
        return False
    # partial_ratio is great for finding a phrase inside a longer sentence
    score = fuzz.partial_ratio(trigger.lower(), command.lower())
    return score >= threshold

def handle_command(command):
    """
    Handles the recognized command.
    Returns True if the assistant should continue listening, False if it should stop.
    """
    if not command:
        return True

    # Enforce wake word "Jarvis"
    # The assistant will only respond if "Jarvis" is detected in the command
    if not is_match(command, 'jarvis', threshold=80):
        print("Ignored: Wake word 'Jarvis' not detected.")
        return True

    if is_match(command, 'hello'):
        speak("Hello! How can I help you today?")
    
    elif is_match(command, 'stop') or is_match(command, 'exit'):
        speak("Goodbye!")
        return False

    elif is_match(command, 'bomb israel'):
        # Assuming the assets folder is in the project root
        video_path = os.path.abspath("assets/bomp.mp4")
        
        if os.path.exists(video_path):
            speak("Roger that. Initiating bomb sequence.")
            # Play the video with mpv and wait for it to finish
            # mpv automatically closes when playback finishes
            subprocess.run(['mpv', video_path])
            
            # Speak after the video finishes
            speak("Target neutralized.")
        else:
            speak("I cannot find the video file. Please make sure bomp.mp4 is in the assets folder.")

    elif is_match(command, 'open my latest project') or is_match(command, 'open latest project'):
        projects_dir = "/home/azya11/source_azya"
        
        if not os.path.exists(projects_dir):
            speak(f"I cannot find the directory {projects_dir}.")
        else:
            try:
                # Get all directories in the projects folder
                dirs = [os.path.join(projects_dir, d) for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
                
                if not dirs:
                    speak("I found no projects in your source directory.")
                else:
                    # Find the latest modified directory
                    latest_project = max(dirs, key=os.path.getmtime)
                    project_name = os.path.basename(latest_project)
                    
                    speak(f"Opening your latest project: {project_name}")
                    subprocess.Popen(['code', latest_project])

                    # Check for git repository and get last commit
                    if os.path.exists(os.path.join(latest_project, ".git")):
                        try:
                            # Get the last commit message (subject only)
                            result = subprocess.run(
                                ['git', 'log', '-1', '--pretty=format:%s'], 
                                cwd=latest_project, 
                                capture_output=True, 
                                text=True,
                                check=True
                            )
                            commit_msg = result.stdout.strip()
                            if commit_msg:
                                speak(f"The last change was: {commit_msg}")
                        except Exception as e:
                            print(f"Git error: {e}")
                            speak("I couldn't read the git history.")
                    else:
                        speak("This project is not a git repository.")
            except Exception as e:
                print(f"Error opening project: {e}")
                speak("I encountered an error while trying to open your project.")

    elif is_match(command, 'play music'):
        speak("Your playlist is always perfect sir.")
        url = "https://music.apple.com/library/playlist/p.6xZa3zxcvX6XEq6"
        
        try:
            # Setup Chrome Options
            chrome_options = Options()
            # Use a dedicated user data directory for Jarvis to persist login
            # This allows Jarvis to run without closing your main Chrome browser
            user_data_dir = os.path.expanduser("~/.config/google-chrome-jarvis")
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_options.add_argument("--start-maximized")
            # Keep browser open after script finishes
            chrome_options.add_experimental_option("detach", True)
            
            # Initialize WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Navigate
            driver.get(url)
            
            # Wait for play button and click
            # Using the selector provided by the user/AI
            try:
                play_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="play-button"]'))
                )
                play_button.click()
                speak("Music started.")
            except Exception as e:
                print(f"Could not find play button: {e}")
                speak("I opened the playlist, but I couldn't find the play button.")
                
        except Exception as e:
            print(f"Error playing music: {e}")
            speak("I encountered an error. Please ensure Google Chrome is completely closed before running this command.")
    
    else:
        # If no specific command is matched, try ChatGPT first
        # Remove "Jarvis" from the query to make it cleaner
        query = command.lower().replace("jarvis", "").strip()
        if query:
            speak("Let me check that for you.")
            response = ask_chatgpt(query)
            
            if response:
                speak(response)
            else:
                # Fallback to Google Search if ChatGPT fails
                speak("I'm having trouble accessing my database. Initiating Google search.")
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                
                # Try to use Selenium to read the result
                try:
                    # Setup Chrome Options
                    chrome_options = Options()
                    user_data_dir = os.path.expanduser("~/.config/google-chrome-jarvis")
                    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
                    chrome_options.add_argument("--start-maximized")
                    chrome_options.add_experimental_option("detach", True)
                    
                    # Initialize WebDriver
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    
                    driver.get(search_url)
                    
                    # Try to find the "AI Overview" or "Featured Snippet"
                    try:
                        # Wait for results
                        time.sleep(2)
                        
                        # Target Featured Snippet (.hgKElc) or Knowledge Panel description (.kno-rdesc span)
                        # Note: AI Overviews (SGE) classes are dynamic, but often appear at the top.
                        # We'll try to grab the most prominent text.
                        snippet = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.hgKElc, div.kno-rdesc span, div[data-attrid='wa:/description']"))
                        )
                        text = snippet.text
                        if text:
                            speak("Here is what I found: " + text)
                        else:
                            speak("I have opened the search results for you.")
                            
                    except Exception:
                        speak("I have opened the search results for you.")

                except Exception as e:
                    print(f"Selenium error (likely profile locked): {e}")
                    # Fallback: Just open the URL in the browser using subprocess
                    # This works even if the profile is locked/busy
                    try:
                        subprocess.Popen(['google-chrome', f"--user-data-dir={user_data_dir}", search_url])
                        speak("I opened the search results for you.")
                    except Exception as sub_e:
                        print(f"Browser error: {sub_e}")
                        speak("I couldn't open the browser.")
    
    return True
