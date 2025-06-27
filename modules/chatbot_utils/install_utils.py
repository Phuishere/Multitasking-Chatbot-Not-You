import os
from huggingface_hub import hf_hub_download

def install_models(folder_name: str = r'llm_models') -> None:
    '''
    A function to install models used in the project.

    '''
    # Define model directories
    MODEL_DIR = os.path.join('.', folder_name)
    os.makedirs(MODEL_DIR, exist_ok=True)
    print(MODEL_DIR)

    # Model download URLs and their corresponding filenames
    model_files = [
        { "repo_id": "Ceenen2302/Llama-3.2-1B-Instruct-GRPO-GGUF", "filename": "Llama-3.2-1B-Instruct-GRPO-GGUF.gguf" },
        { "repo_id": "unsloth/Llama-3.2-1B-Instruct-GGUF", "filename": "Llama-3.2-1B-Instruct-Q8_0.gguf" },
        { "repo_id": "unsloth/Llama-3.2-3B-Instruct-GGUF", "filename": "Llama-3.2-3B-Instruct-Q8_0.gguf" }
    ]

    # Download each model file
    for model_file in model_files:
        try:
            # Get repo id and file name from list
            repo_id = model_file["repo_id"]
            filename = model_file["filename"]
            
            file_path = os.path.join(MODEL_DIR, filename)
            print("_____________________________________________________________")
            print("_____________________________________________________________\n")
            print(f"\n\n----- Downloading {filename} -----\n")
            if not os.path.exists(file_path):
                hf_hub_download(repo_id = repo_id, filename = filename, local_dir = MODEL_DIR)
                print(f"\n✅✅✅ Downloaded {filename} to {file_path}!\n\n")
            else:
                print(f"\n✅✅✅ {filename} already exists at {file_path}\n\n")
        except:
            pass
    print("_____________________________________________________________")
    print("_____________________________________________________________\n")