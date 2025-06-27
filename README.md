# A demo of Streamlit app with LLMs

### This repo uses LLaMa CPP Python-binding API library to inference
- The models are in .gguf format (downloaded from Hugging Face).
- llama_cpp_python can also be used for agentic AI, especially the llama_cpp_agent library.
- The output of model in respond() function can be streamed word by word using llama_cpp's function. Need to find a way to incorporate it (streaming function) with Restful API - or just use Streamlit.

### Streamlit is used as a demo for this model
- Has temporary memory (will be lost if reload)
- Show streamed output of model

### Set-up
1. **Env**
- Python version: 3.11.9
- Dependencies:
```
python -m venv env
./env/Scripts/activate.bat
pip install -r requirements.txt
```

2. **Model**
- Run the script ```streamlit run main.py``` to automatically download the model.

3. **C++ and Visual Studio** may need to be installed

4. Further guides would be available. Currently, some experiences in setting up the environment and code is in "stt_pj_exp.txt".

### Future development
1. Llama CPP Server (?)
    - Separating the endpoint with streamlit
    - **Avoiding init models everytime**
    - Multi-user use-case
    - Make the system more scalable

2. Whisper AI for online transcripting purpose

3. A more complex agentic system using MCP:
    - Fix functions: email (parsing JSON), Googling (DuckDuckGo is limited)
    - More functions: RAG (try using PostgreSQL as vector database? instead of LLaMa Index?), etc.
    - Other mini and trivial function:
        + Multi-modal: a Coca model to describe text or using the built-in multi-modal models
        + Test out the reasoning-function calling paper (with reasoning chain associated with functions)

4. Dockerize the project

5. Package it (?)

6. Trivia:
    - Add memory using Database for the model
    - Testing Jan-Nano function calling and searching ability
    - Reimplementing prompts and agentic features from scratch