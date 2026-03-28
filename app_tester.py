import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor

# ---------------- CONFIGURATION ----------------
# REPLACE with your EC2 Public IP or 'localhost' if running locally
APP_URL = "http://54.204.162.28:8080/get"

# Medical questions to simulate user traffic
TEST_QUESTIONS = [
    "What are the symptoms of a heart attack?",
    "I have a severe headache and sensitivity to light, what could it be?",
    "How do I treat a minor burn at home?",
    "What is the difference between a cold and the flu?",
    "Can you list the side effects of Ibuprofen?",
    "I have a persistent dry cough for 3 weeks.",
    "What are the early signs of diabetes?",
    "Is it safe to take paracetamol on an empty stomach?",
    "Remedies for seasonal allergies",
    "When should I see a doctor for back pain?"
]

def ask_chatbot(question, user_id):
    """Sends a single question to the chatbot and prints the response."""
    print(f"[User {user_id}] asking: '{question}'")
    
    try:
        # The app expects form data with key 'msg'
        start_time = time.time()
        response = requests.post(APP_URL, data={"msg": question}, timeout=30)
        duration = round(time.time() - start_time, 2)

        if response.status_code == 200:
            print(f"✅ [User {user_id}] received answer in {duration}s: {response.text[:60]}...")
        else:
            print(f"❌ [User {user_id}] Error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ [User {user_id}] Connection failed: {e}")

def run_load_test(users=3):
    """Simulates concurrent users asking questions."""
    print(f"🚀 Starting load test with {users} concurrent users on {APP_URL}...\n")
    
    with ThreadPoolExecutor(max_workers=users) as executor:
        # random.sample ensures we pick unique questions for this batch
        selected_questions = random.sample(TEST_QUESTIONS, min(len(TEST_QUESTIONS), users * 2))
        
        futures = []
        for i in range(len(selected_questions)):
            user_id = (i % users) + 1
            # Add a tiny delay to simulate realistic staggering
            time.sleep(random.uniform(0.1, 1.0)) 
            futures.append(executor.submit(ask_chatbot, selected_questions[i], user_id))

    print("\n🏁 Test complete.")

if __name__ == "__main__":
    # Run with 3 simulated concurrent users
    run_load_test(users=3)
