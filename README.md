# End-to-End-Medical-Chatbot-Generative-AI
# How to run?
### STEPS:

Clone the repository

```bash
Project repo: https://github.com/Kibs-Neville/end-to-end-medical-chatbot.git
```

### STEP 01 - Create a conda environment after opening the repository

```bash
conda create -n medibot python=3.10 -y
```

```bash
conda activate medibot
```

### STEP 02 - Install the requirements

```bash
pip install -r requirements.txt
```

### Create a .env file in the root directory and add your Pinecone & Grok API Keys as follows:

```bash
PINECONE_API_KEY = "xxxxxxxxxxxxx"
GROQ_API_KEY = "xxxxxxxxxxxxxxx"
```