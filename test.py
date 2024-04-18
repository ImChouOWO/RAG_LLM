import torch
from sentence_transformers import SentenceTransformer, util
import os
# # load the large language model file
from llama_cpp import Llama




# Function to get relevant context from the vault based on user input
def get_relevant_context(user_input, vault_embeddings, vault_content, model, top_k=3):
    if vault_embeddings.size <= 0:  # Check if the tensor has any elements
        return []
    # Encode the user input
    input_embedding = model.encode([user_input])
    # Compute cosine similarity between the input and vault embeddings
    cos_scores = util.cos_sim(input_embedding, vault_embeddings)[0]
    # Adjust top_k if it's greater than the number of available scores
    top_k = min(top_k, len(cos_scores))
    # Sort the scores and get the top-k indices
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    # Get the corresponding context from the vault

    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    
    return relevant_context

def chat(user_input, system_message, vault_embeddings, vault_content, model):
    relevant_context = get_relevant_context(user_input, vault_embeddings, vault_content, model)
    print(f"relevant text：{relevant_context}")
    LLM = Llama(model_path="model\mistral-7b-instruct-v0.1.Q5_K_M.gguf")
    prompt = f"role:{system_message},Q:{relevant_context}\n\n{user_input}"
    output = LLM(prompt)
    print(output["choices"][0]["text"])


if __name__ == "__main__":
    model = SentenceTransformer("all-MiniLM-L6-v2")
    user_input =input("ask：")
    vault_content = [ """
                    Once in the small, whimsical town of Maplewood, nestled between the whispering forests and the shimmering lake, there lived a young girl named Ellie. Ellie had a peculiar talent for understanding the language of the wind. Each gust, each gentle breeze carried messages that only she could decipher.

                    One blustery autumn day, as leaves danced like golden flames around her, the wind brought Ellie an urgent plea for help. The Guardian of the Forest, an ancient oak known as Old Thorn, was dying. Without his strength to anchor it, the forest was beginning to wither.

                    Determined to help, Ellie ventured into the heart of the woods. The trees, recognizing her as a friend, pointed the way with their rustling leaves. After hours of walking, she finally found Old Thorn, his trunk marred by a mysterious symbol.

                    Remembering old tales her grandmother had shared, Ellie realized that the symbol was that of a binding curse. Someone wanted to harm the forest. To break the curse, she needed the Silver Water from the lake, which shimmered under the light of the full moon.

                    As the moon rose, casting a silver glow across the night, Ellie rushed to the lake's edge. Dipping a leaf into the water, she watched as it turned to silver. She hurried back, the precious leaf cupped gently in her hands.

                    Upon returning, Ellie pressed the leaf against Old Thorn's trunk. A warm light spread from the symbol, melting it away. The Guardian's leaves, once withering, burst forth in a vibrant cascade of green.

                    The forest sighed in relief, a chorus that resonated in Ellie's heart. From that day on, she became the Keeper of Whispers, a guardian who listened to the wind and protected the harmony between Maplewood and the living forest. And the wind, in return, whispered tales of the brave girl to those who would listen.
                    """]
    
    vault_embeddings = model.encode(vault_content) if vault_content else []
    vault_embeddings_tensor = torch.tensor(vault_embeddings) 
    print(vault_embeddings_tensor)
    system_message = "You are a helpful assistat that is an expert at extracting the most useful information from a given text"
    chat(user_input, system_message, vault_embeddings, vault_content, model)


