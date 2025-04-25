# CLI Chatbot with Gemini API

This is a **Command-Line Interface (CLI) chatbot** powered by Google's **Gemini API**. It facilitates natural conversations and collects user feedback at the end.

## 🚀 Features
- Handles user messages and responds intelligently.
- Detects **exit intent** and prompts for feedback.
- Supports **function calling** to collect structured reviews and ratings.
- Saves user feedback to a local file (`feedback.txt`).

## 🛠️ Setup Instructions
### 1️⃣ Clone the Repository

git clone <https://github.com/imazk/CLI-based-Chat-Application.git>

### 2️⃣ Install Dependencies
Ensure you have **Python 3.10+** installed, then run:
```
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your-api-key-here
```
Your `.env` file is **ignored** via `.gitignore`, ensuring security.

## 📜 Usage
Run the chatbot using:
```
python cli_chat.py
```
You'll see:
```
Welcome to the CLI Chatbot! Type your messages below.
> 
```
Start chatting! To exit, simply type:
- **"bye"**
- **"exit"**
- **"end chat"**
- **"I want to leave"**

Before closing, the chatbot will ask for a **review and rating (1-5).**

## 📝 Example Interaction
```
Welcome to the CLI Chatbot! Type your messages below.
> Hi
CLI ChatBot: Hi there! How can I help you today?

> Tell me a joke.
CLI ChatBot: Why don't scientists trust atoms?

Because they make up everything!

> Haha good one thanks.
CLI ChatBot: Glad I could give you a laugh! 😊

> yeah thanks
Say bye, exit, or end chat, If you want to leave the chat.
CLI ChatBot: You're welcome! Is there anything else I can help you with?

> exit
Say bye, exit, or end chat, If you want to leave the chat.
ChatBot: Before you leave, Kindly give your feedback.
Your feedback: I like the joke
Rate your chat experience (1-5): 5
Thank you! Your feedback has been saved.
```

