import json
import os


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def generate_prompt(chat_prompt: str=None) -> str:
    """
    Build final input prompt.
    :param prompt: str, system and user prompts
    :param chat_prompt: str, slack chat prompt 
    :return: str, combined prompts for LLM request 
    """
    # Load prompts from JSON file
    file_path = os.path.join(CURRENT_DIRECTORY, 'prompts.json')
    with open(file_path, 'r') as f:
        prompts = json.load(f)

    # Converting role headers to python to utilize formatting 
    HEADER_ID = prompts["HEADER_ID"]
    HEADER_ID_SYS = eval(prompts["HEADER_ID_SYS"])
    HEADER_ID_USER = eval(prompts["HEADER_ID_USER"])
    HEADER_ID_ASSIST = eval(prompts["HEADER_ID_ASSIST"])
    
    # Assign special tokens to system and user prompt
    sys_prompt = prompts["system"].format_map({
        'B_TEXT': prompts["B_TEXT"],
        'HEADER_ID_SYS': HEADER_ID_SYS,
        'EOT_ID': prompts["EOT_ID"]
    })
    user_prompt = prompts["user"].format_map({
        'HEADER_ID_USER': HEADER_ID_USER,
        'EOT_ID': prompts["EOT_ID"]
    })

    # Use default tips prompt if no chat prompt is provided
    chat_prompt = prompts["tips"] if chat_prompt is None else chat_prompt

    return f"{sys_prompt}{user_prompt}{chat_prompt}\n\n{HEADER_ID_ASSIST}"