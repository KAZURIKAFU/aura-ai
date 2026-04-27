"""
LLM Engine — AuraAI Personal Assistant
Author: Abhay Sharma | github.com/KAZURIKAFU
Rule-based + pattern matching conversational AI engine with memory
"""

import re
import math
import random
from datetime import datetime
from memory import ConversationMemory

# ── Knowledge Base ────────────────────────────────────────────────────────────
KNOWLEDGE = {
    # AI & Tech
    "what is machine learning": "Machine Learning is a subset of AI that enables systems to learn from data and improve without being explicitly programmed. It includes supervised, unsupervised, and reinforcement learning.",
    "what is deep learning": "Deep Learning uses neural networks with many layers to learn complex patterns. It powers image recognition, NLP, and speech recognition systems.",
    "what is nlp": "Natural Language Processing (NLP) is a branch of AI focused on enabling computers to understand, interpret, and generate human language.",
    "what is iot": "The Internet of Things (IoT) refers to a network of physical devices embedded with sensors and software that connect and exchange data over the internet.",
    "what is generative ai": "Generative AI creates new content — text, images, code, audio — by learning patterns from training data. Examples include GPT, DALL-E, and Gemini.",
    "what is bigquery": "Google BigQuery is a serverless, highly scalable cloud data warehouse that enables super-fast SQL queries using Google's infrastructure.",
    "what is vertex ai": "Vertex AI is Google Cloud's unified ML platform for building, deploying, and scaling ML models using Google Cloud infrastructure.",
    "what is mlops": "MLOps (Machine Learning Operations) combines ML, DevOps, and data engineering to streamline the deployment and maintenance of ML models in production.",
    "what is a llm": "A Large Language Model (LLM) is an AI model trained on massive text datasets to understand and generate human language. Examples: GPT-4, Gemini, Claude.",
    "what is python": "Python is a high-level, interpreted programming language known for its simplicity. It's widely used in data science, AI, web development, and automation.",
    "what is pandas": "Pandas is a Python library for data manipulation and analysis. It provides data structures like DataFrames for working with structured data.",
    "what is spark": "Apache Spark is an open-source distributed computing framework for processing large-scale data fast. It's widely used in big data pipelines.",
    "what is hadoop": "Apache Hadoop is an open-source framework for distributed storage and processing of large datasets using clusters of computers.",
    # Data Science
    "what is data science": "Data Science combines statistics, programming, and domain expertise to extract insights from data. It includes data collection, cleaning, analysis, visualization, and ML.",
    "what is a neural network": "A neural network is a computational model inspired by the human brain, consisting of layers of interconnected nodes (neurons) that process and learn from data.",
    "what is random forest": "Random Forest is an ensemble ML algorithm that builds multiple decision trees and combines their predictions. It's highly accurate and resistant to overfitting.",
    "what is svm": "Support Vector Machine (SVM) is a supervised ML algorithm that finds the optimal hyperplane to separate classes in high-dimensional space.",
    "what is overfitting": "Overfitting occurs when an ML model learns training data too well, including noise, and performs poorly on new unseen data. Solutions include regularization and more data.",
    "what is a confusion matrix": "A confusion matrix is a table showing the performance of a classification model — true positives, false positives, true negatives, and false negatives.",
    # Cybersecurity
    "what is a dos attack": "A Denial of Service (DoS) attack floods a target with traffic to overwhelm resources and make services unavailable to legitimate users.",
    "what is a ddos attack": "A Distributed DoS (DDoS) attack uses multiple systems (often a botnet) to simultaneously flood a target, making it much harder to block.",
    "what is sql injection": "SQL Injection is a cyberattack where malicious SQL code is inserted into input fields to manipulate a database — one of the most common web vulnerabilities.",
    "what is a firewall": "A firewall is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules.",
    "what is encryption": "Encryption converts data into an unreadable format using algorithms and keys. Only authorized parties with the correct key can decrypt and read the data.",
    # General
    "what is cloud computing": "Cloud computing delivers computing services — servers, storage, databases, networking, software — over the internet on a pay-as-you-go basis.",
    "what is blockchain": "Blockchain is a distributed ledger technology that records transactions across multiple computers in a way that makes them tamper-resistant.",
    "what is quantum computing": "Quantum computing uses quantum mechanics to perform computations exponentially faster than classical computers for certain problem types.",
}

GREETINGS   = ["hello","hi","hey","good morning","good afternoon","good evening","sup","what's up"]
FAREWELLS   = ["bye","goodbye","see you","take care","cya","later","farewell"]
THANKS      = ["thank you","thanks","thank u","thx","appreciate it","cheers"]
ABOUT_ME    = ["who are you","what are you","tell me about yourself","introduce yourself",
               "what can you do","your name","what's your name"]

# ── Tool Functions ────────────────────────────────────────────────────────────
def _calculate(expr: str) -> str:
    """Safe math expression evaluator."""
    try:
        clean = re.sub(r'[^0-9+\-*/().% ]', '', expr)
        if not clean.strip():
            return "❌ Invalid expression."
        result = eval(clean, {"__builtins__": {}},
                      {"sqrt": math.sqrt, "pi": math.pi, "e": math.e,
                       "sin": math.sin, "cos": math.cos, "tan": math.tan,
                       "log": math.log, "abs": abs, "pow": pow, "round": round})
        return f"🔢 **Result:** `{clean}` = **{round(result, 6)}**"
    except Exception as e:
        return f"❌ Calculation error: {str(e)}"


def _write_email(context: str) -> str:
    """Generate a professional email template."""
    return f"""📧 **Professional Email Template:**

---
**Subject:** [Add relevant subject]

Dear [Recipient Name],

I hope this message finds you well.

{context.strip()}

Please feel free to reach out if you have any questions or require further information.

Best regards,
Abhay Sharma
📧 abby.official2412@gmail.com
🔗 linkedin.com/in/abhay-sharma-426702208
---
*Feel free to customize this template!*"""


def _summarize(text: str) -> str:
    """Summarize text by extracting key points."""
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 20]
    if not sentences:
        return "❌ Please provide more text to summarize."
    key_points = sentences[:min(4, len(sentences))]
    summary = "\n".join([f"• {s}." for s in key_points])
    return f"📝 **Summary ({len(sentences)} sentences → {len(key_points)} key points):**\n\n{summary}"


def _define_word(word: str) -> str:
    """Check knowledge base for definition."""
    w = word.lower().strip()
    for key, val in KNOWLEDGE.items():
        if w in key or any(w in k for k in key.split()):
            return f"📖 **{word.title()}:**\n\n{val}"
    return f"❓ I don't have a specific definition for **{word}** in my knowledge base. Try asking 'What is {word}?'"


def _generate_code(task: str) -> str:
    """Generate simple Python code snippets."""
    task_lower = task.lower()
    if "hello world" in task_lower:
        code = 'print("Hello, World!")'
    elif "fibonacci" in task_lower:
        code = """def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=' ')
        a, b = b, a + b

fibonacci(10)"""
    elif "sort" in task_lower or "bubble" in task_lower:
        code = """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

print(bubble_sort([64, 34, 25, 12, 22]))"""
    elif "factorial" in task_lower:
        code = """def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # Output: 120"""
    elif "palindrome" in task_lower:
        code = """def is_palindrome(s):
    s = s.lower().replace(' ', '')
    return s == s[::-1]

print(is_palindrome("racecar"))  # True
print(is_palindrome("hello"))    # False"""
    elif "dataframe" in task_lower or "pandas" in task_lower:
        code = """import pandas as pd

# Create a DataFrame
data = {
    'Name':  ['Alice', 'Bob', 'Charlie'],
    'Score': [95, 82, 78],
    'Grade': ['A', 'B', 'C']
}
df = pd.DataFrame(data)
print(df)
print(df.describe())"""
    elif "read csv" in task_lower:
        code = """import pandas as pd

df = pd.read_csv('data.csv')
print(df.head())
print(f'Shape: {df.shape}')
print(df.info())"""
    elif "plot" in task_lower or "chart" in task_lower or "graph" in task_lower:
        code = """import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values':   [23, 45, 12, 67]
})

fig = px.bar(df, x='Category', y='Values',
             title='My Chart',
             color='Values',
             color_continuous_scale='Blues')
fig.show()"""
    elif "machine learning" in task_lower or "ml model" in task_lower:
        code = """from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Generate sample data
X = np.random.rand(200, 5)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

# Split & train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
acc = accuracy_score(y_test, model.predict(X_test))
print(f'Accuracy: {acc:.2%}')"""
    else:
        code = f"""# Python solution for: {task}

def solution():
    # TODO: Implement your solution here
    print("Hello from AuraAI!")
    result = []
    # Add your logic here
    return result

if __name__ == "__main__":
    output = solution()
    print(f"Result: {{output}}")"""

    return f"```python\n{code}\n```\n\n💡 *Copy this code and run it in your Python environment!*"


# ── Main Engine ───────────────────────────────────────────────────────────────
class AuraEngine:
    def __init__(self):
        self.memory = ConversationMemory()
        self.turn   = 0

    def respond(self, user_input: str) -> dict:
        """Generate a response to user input."""
        self.turn += 1
        raw   = user_input.strip()
        query = raw.lower().strip().rstrip("?!.")
        now   = datetime.now()

        # ── Math — check BEFORE greeting to avoid 'what is X' conflicts
        has_operator = any(op in raw for op in ['+','-','*','/'])
        has_number   = bool(__import__('re').search(r'\d', raw))
        calc_words   = ['calculate','compute','how much is']
        if (has_operator and has_number) or any(w in query for w in calc_words):
            expr = __import__('re').search(r'[\d\s\+\-\*/\(\)\.%]+', raw)
            if expr and expr.group().strip() and has_number:
                result = _calculate(expr.group().strip())
                self.memory.add(raw, result)
                return {'response': result, 'type': 'calculation', 'confidence': 0.95}

        # ── Greeting ──
        if any(g == query or query.startswith(g+' ') for g in GREETINGS) and len(query.split()) <= 3:
            hour = now.hour
            time_greet = ("Good morning" if hour < 12 else
                          "Good afternoon" if hour < 17 else "Good evening")
            responses = [
                f"{time_greet}! 👋 I'm **AuraAI**, your intelligent assistant. How can I help you today?",
                f"Hey there! 😊 Great to see you! I'm **AuraAI**. What can I help you with?",
                f"Hello! 🌟 I'm **AuraAI**, powered by advanced NLP. Ask me anything!",
            ]
            msg = random.choice(responses)
            self.memory.add(raw, msg)
            return {"response": msg, "type": "greeting", "confidence": 1.0}

        # ── Farewell ──
        if any(f in query for f in FAREWELLS):
            msg = "Goodbye! 👋 It was great chatting with you. Come back anytime! 🌟"
            self.memory.add(raw, msg)
            return {"response": msg, "type": "farewell", "confidence": 1.0}

        # ── Thanks ──
        if any(t in query for t in THANKS):
            responses = ["You're welcome! 😊 Happy to help!", "Anytime! 🌟 That's what I'm here for!",
                         "Glad I could help! 🎉 Let me know if you need anything else!"]
            msg = random.choice(responses)
            self.memory.add(raw, msg)
            return {"response": msg, "type": "thanks", "confidence": 1.0}

        # ── About Me ──
        if any(a in query for a in ABOUT_ME):
            msg = """🤖 **I'm AuraAI** — your intelligent personal assistant!

**What I can do:**
• 💬 Answer questions on AI, Data Science, Cybersecurity & Tech
• 🔢 Solve math problems — just say "calculate 15 * 8 + 32"
• 🐍 Generate Python code — say "write code for fibonacci"
• 📧 Draft professional emails — say "write email about meeting"
• 📝 Summarize text — say "summarize: [your text]"
• 🧠 Remember our conversation context
• ❓ Answer general knowledge questions

**Built by:** Abhay Sharma | Manipal University Jaipur
**Tech:** Python, Dash, NLP, LangChain-style Memory"""
            self.memory.add(raw, msg)
            return {"response": msg, "type": "about", "confidence": 1.0}

        # ── Math / Calculate ──
        if any(w in query for w in ["calculate","compute","what is","solve","=","math",
                                     "how much is","add","subtract","multiply","divide"]):
            expr_match = re.search(r'[\d\s\+\-\*/\(\)\.%sqrt]+', raw)
            if expr_match and any(op in raw for op in ['+','-','*','/','^','sqrt']):
                result = _calculate(expr_match.group())
                self.memory.add(raw, result)
                return {"response": result, "type": "calculation", "confidence": 0.95}

        # ── Code Generation ──
        if any(w in query for w in ["write code","generate code","code for","python code",
                                     "how to code","program for","script for","write a program",
                                     "write python","show code"]):
            code_topic = re.sub(r'(write code|generate code|code for|python code|'
                                r'write python|write a program|program for|script for|'
                                r'show code|how to code)\s*(for|to|about|a|an)?\s*', '', query).strip()
            result = _generate_code(code_topic or raw)
            self.memory.add(raw, result)
            return {"response": result, "type": "code", "confidence": 0.95}

        # ── Email Writing ──
        if any(w in query for w in ["write email","draft email","compose email",
                                     "write a mail","email template"]):
            context = re.sub(r'(write email|draft email|compose email|'
                             r'write a mail|email template)\s*(about|for|regarding)?\s*', '', query).strip()
            result = _write_email(context or "I am writing to follow up on our previous discussion.")
            self.memory.add(raw, result)
            return {"response": result, "type": "email", "confidence": 0.95}

        # ── Summarize ──
        if "summarize" in query or "summary of" in query or "summarise" in query:
            text = re.sub(r'(summarize|summary of|summarise):?\s*', '', raw, flags=re.IGNORECASE).strip()
            result = _summarize(text) if text else "📝 Please provide the text you'd like me to summarize after 'summarize:'"
            self.memory.add(raw, result)
            return {"response": result, "type": "summary", "confidence": 0.95}

        # ── Define ──
        if query.startswith("define ") or query.startswith("what is ") or query.startswith("explain "):
            result = _define_word(re.sub(r'^(define|what is|explain)\s+', '', query))
            if "don't have" not in result:
                self.memory.add(raw, result)
                return {"response": result, "type": "definition", "confidence": 0.9}

        # ── Knowledge Base Search ──
        best_match, best_score = None, 0
        query_words = set(query.split())
        for key, val in KNOWLEDGE.items():
            key_words  = set(key.split())
            score = len(query_words & key_words) / max(len(key_words), 1)
            if score > best_score:
                best_score, best_match = score, val
        if best_score > 0.3 and best_match:
            self.memory.add(raw, best_match)
            return {"response": f"📖 {best_match}", "type": "knowledge", "confidence": best_score}

        # ── Date/Time ──
        if any(w in query for w in ["time","date","today","day","year","month"]):
            msg = f"🕐 **Current Date & Time:**\n\n📅 Date: **{now.strftime('%A, %B %d, %Y')}**\n⏰ Time: **{now.strftime('%I:%M %p')}**"
            self.memory.add(raw, msg)
            return {"response": msg, "type": "datetime", "confidence": 1.0}

        # ── Previous Context ──
        context = self.memory.get_context()
        if context and len(context) > 0:
            last = context[-1]
            if any(w in query for w in ["more","elaborate","explain more","tell me more","go on","continue"]):
                msg = f"📌 **Continuing from our previous discussion:**\n\n{last['response']}\n\n💡 Would you like me to go deeper on any specific aspect?"
                self.memory.add(raw, msg)
                return {"response": msg, "type": "continuation", "confidence": 0.7}

        # ── Fallback ──
        fallbacks = [
            f"🤔 I'm not sure I fully understand **\"{raw}\"**. Could you rephrase?\n\n💡 **Try asking:**\n• *What is machine learning?*\n• *Calculate 25 * 4*\n• *Write code for fibonacci*\n• *Write email about project update*\n• *Summarize: [your text]*",
            f"❓ Hmm, I don't have a specific answer for that yet. Try asking about **AI, Data Science, Cybersecurity, or Tech topics**!\n\n💡 Or try: *calculate*, *write code*, *write email*, or *define [term]*",
            f"🌟 That's an interesting question! I'm still learning. Try asking about **machine learning, IoT, BigQuery, Gemini AI**, or ask me to **generate Python code**!",
        ]
        msg = random.choice(fallbacks)
        self.memory.add(raw, msg)
        return {"response": msg, "type": "fallback", "confidence": 0.3}
