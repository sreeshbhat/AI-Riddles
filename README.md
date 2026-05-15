# AI Vault: Riddles Edition 🧩

A multi-level riddle challenge where solving each puzzle unlocks a part of the final vault code.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure API Key**:
   - Ensure you have a `.env` file with `COHERE_API_KEY=your_key`.
3. **Run the App**:
   ```bash
   python -m streamlit run streamlit_app.py
   ```

## How to Play

- **Solve Riddles**: You will be presented with a series of riddles.
- **Unlock Parts**: Each correct answer reveals a word for the final vault code (visible in the sidebar).
- **Get Hints**: If you are stuck, the AI Riddle Guardian (powered by Cohere) will give you a cryptic hint.
- **Final Unlock**: Once all riddles are solved, combine the unlocked words to open the vault!

## Educational Value
This project demonstrates:
- **Sequential Puzzles**: Progressing through different states of an application.
- **AI-Powered Hints**: Using AI to provide contextual help without spoiling answers.
- **Dynamic UI**: Updating the sidebar and main screen based on player progress.
