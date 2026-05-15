import streamlit as st
import cohere
import os
from dotenv import load_dotenv

# Load local .env for local testing
load_dotenv()

# --- CONFIG ---
st.set_page_config(page_title="AI Vault: Riddles Edition", page_icon="🧩")

# --- API KEY SETUP ---
def get_api_key():
    api_key = os.getenv("COHERE_API_KEY")
    if api_key: return api_key
    try:
        if "COHERE_API_KEY" in st.secrets:
            return st.secrets["COHERE_API_KEY"]
    except: pass
    return None

api_key = get_api_key()
if not api_key:
    st.error("COHERE_API_KEY not found. Please set it in your .env file or Streamlit Secrets.")
    st.stop()

co = cohere.Client(api_key=api_key)

# --- GAME DATA ---
RIDDLES = [
    {
        "riddle": "I split words into smaller pieces so transformers can understand language. I turn 'unbelievable' into chunks. What am I?",
        "answer": "tokenizer",
        "reward": "ATTENTION"
    },
    {
        "riddle": "I decide which words in a sentence matter most to each other. Without me, transformers lose context. What am I?",
        "answer": "self attention",
        "reward": "IS"
    },
    {
        "riddle": "I store learned patterns inside billions of floating-point values. Larger models usually have more of me. What am I?",
        "answer": "parameters",
        "reward": "ALL"
    },
    {
        "riddle": "I predict the next token one step at a time during text generation. Temperature and sampling affect me. What process am I?",
        "answer": "decoding",
        "reward": "YOU"
    },
    {
        "riddle": "I allow a model to remember earlier tokens in long sequences by encoding their order mathematically. What am I?",
        "answer": "positional encoding",
        "reward": "NEED"
    },
    {
        "riddle": "I make language models solve complex problems step by step instead of jumping directly to the final answer. What prompting technique am I?",
        "answer": "chain of thought",
        "reward": "TO"
    },
    {
        "riddle": "I compress massive datasets into vector representations so semantic similarity can be searched quickly. What am I called?",
        "answer": "embedding",
        "reward": "OPEN"
    },
    {
        "riddle": "I am the training process where humans rank responses and the model learns preferred behavior from feedback. What am I?",
        "answer": "rlhf",
        "reward": "THE"
    },
    {
        "riddle": "I identify whether a piece of text expresses positive, negative, or neutral emotion. What NLP task am I?",
        "answer": "sentiment analysis",
        "reward": "VAULT"
    }, 
    {
        "riddle": "I am the famous 2017 paper that introduced the transformer architecture to the world. Name the paper.",
        "answer": "attention is all you need",
        "reward": "NOW"
    }
]

FINAL_CODE = "ATTENTION IS ALL YOU NEED TO OPEN THE VAULT NOW"

# --- SESSION STATE ---
if "current_level" not in st.session_state:
    st.session_state.current_level = 0
if "unlocked_words" not in st.session_state:
    st.session_state.unlocked_words = []
if "history" not in st.session_state:
    st.session_state.history = []
if "won" not in st.session_state:
    st.session_state.won = False

# --- UI ---
st.title("🧩 AI Vault: Riddles Edition")
st.markdown("### Solve riddles to unlock the final vault code.")

# Sidebar Progress
with st.sidebar:
    st.header("Vault Progress")
    st.write(f"Level: {st.session_state.current_level + 1} / {len(RIDDLES) + 1}")
    
    st.subheader("Unlocked Code Parts:")
    if st.session_state.unlocked_words:
        for word in st.session_state.unlocked_words:
            st.success(word)
    else:
        st.info("No parts unlocked yet.")

    if st.button("Reset Game"):
        for key in ["current_level", "unlocked_words", "history", "won"]:
            if key in st.session_state: del st.session_state[key]
        st.rerun()

# --- GAME LOGIC ---

# 1. Check for Victory
if st.session_state.won:
    st.balloons()
    st.success(f"🏆 VAULT OPENED! The final phrase was: {FINAL_CODE}")
    st.stop()

# 2. Level Routing
if st.session_state.current_level < len(RIDDLES):
    # Riddle Level
    current_puzzle = RIDDLES[st.session_state.current_level]
    st.info(f"**RIDDLE:** {current_puzzle['riddle']}")
    
    # Display Chat History for the current riddle
    for message in st.session_state.history:
        with st.chat_message(message["role"].lower().replace("chatbot", "assistant")):
            st.write(message["message"])

    if prompt := st.chat_input("Enter your answer..."):
        # Check answer
        if prompt.lower().strip() == current_puzzle["answer"].lower():
            st.session_state.unlocked_words.append(current_puzzle["reward"])
            st.session_state.current_level += 1
            st.session_state.history = [] # Clear history for next level
            st.toast(f"Correct! '{current_puzzle['reward']}' unlocked.")
            st.rerun()
        else:
            # Failed attempt - Get AI Guardian Feedback
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Guardian is providing a hint..."):
                    system_prompt = (
                        "You are the Riddle Guardian. "
                        f"The current riddle is: '{current_puzzle['riddle']}'. "
                        f"The correct answer is: '{current_puzzle['answer']}'. "
                        "The user gave an incorrect answer. Provide a subtle, "
                        "cryptic hint to help them solve it without giving the answer away."
                    )
                    try:
                        # CONTEXT WINDOW MANAGEMENT: 
                        # We limit history to the last 6 messages (3 turns) to stay within 
                        # the model's window and demonstrate token management.
                        response = co.chat(
                            message=f"My answer is: '{prompt}'",
                            chat_history=st.session_state.history[-6:],
                            preamble=system_prompt
                        )
                        ai_text = response.text
                        st.write(ai_text)
                        st.session_state.history.append({"role": "USER", "message": prompt})
                        st.session_state.history.append({"role": "CHATBOT", "message": ai_text})
                    except Exception as e:
                        st.error(f"AI Error: {e}")

else:
    # Final Vault Level
    st.warning("🔒 **FINAL CHALLENGE:** Combine the unlocked parts to open the vault.")
    st.write("Enter the full final phrase (all 3 words):")
    
    final_guess = st.text_input("Final Code...", key="final_input")
    if st.button("Unlock Vault"):
        if final_guess.upper().strip() == FINAL_CODE:
            st.session_state.won = True
            st.rerun()
        else:
            st.error("Incorrect. Look at the sidebar for your unlocked parts!")

