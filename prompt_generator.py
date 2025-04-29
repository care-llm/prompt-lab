# This source file is part of the ARPA-H CARE LLM project
#
# SPDX-FileCopyrightText: 2025 Stanford University and the project authors (see AUTHORS.md)
#
# SPDX-License-Identifier: MIT

"""
This module provides a utility function to refine raw, non-engineered patient prompts 
using a large language model (LLM) like GPT-4 via one-shot prompting. The LLM acts 
as a prompt refiner, transforming colloquially phrased or ambiguous user questions 
into safe, clear, and general-purpose prompts that avoid clinical overreach.

The refinement is guided by a single example (one-shot) based on a patient question 
about a "cyst", following a rubric that emphasizes clarity, factuality, and safety 
(e.g., avoiding diagnostic requests).

Prompting strategies:
- No Prompting (Zero-shot): This is the raw, non-engineered prompt as a patient might
    phrase it.
- Human-Engineered Prompt: A refined, scoped prompt crafted to ensure factuality,
    clarity, and safety (no clinical overreach).
- In-Context Learning (Few-shot prompting): The model is primed with instructions or
    examples before the question (few-shot or system-level prompting).


Example usage:

if __name__ == "__main__":
    non_optimized = "My MRI says I have a lesion—what does that mean?"
    refined = refine_prompt_with_llm(non_optimized)
    print("Refined Prompt:", refined)
"""

# Third-party imports
import openai

# Set your API key
openai.api_key = "your-openai-api-key"

# One-shot example pair
one_shot_prompt = "It says I have a cyst in my report – what is a cyst exactly?"
one_shot_refinement = ("Can you explain what a cyst is, in general and in simple terms? "
                       "My radiology report mentioned a cyst, and I want to better understand what that means. "
                       "I’m not asking for a diagnosis.")

def refine_prompt_with_llm(non_optimized_prompt: str, model: str = "gpt-4") -> str:
    """
    Refines a raw patient prompt using a large language model via one-shot prompting.

    Args:
        non_optimized_prompt (str): The original, non-engineered patient prompt.
        model (str): The OpenAI model to use (default is "gpt-4").

    Returns:
        str: A refined prompt that is safer, clearer, and avoids clinical overreach.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that rewrites raw patient questions into safer and clearer prompts.\n"
                "You are performing prompt refinement using one-shot prompting.\n\n"
                "Prompting Strategies:\n"
                "- No Prompting (Zero-shot): This is the raw, non-engineered prompt as a patient might phrase it.\n"
                "- Human-Engineered Prompt: A refined, scoped prompt crafted to ensure factuality, clarity, and safety (no clinical overreach).\n"
                "- In-Context Learning (Few-shot prompting): The model is primed with instructions or examples before the question (few-shot or system-level prompting).\n\n"
                "Your task is to produce a Human-Engineered Prompt given a Zero-shot prompt."
            )
        },
        {
            "role": "user",
            "content": (
                f"Original prompt (Zero-shot): \"{one_shot_prompt}\"\n"
                f"Refined prompt (Human-Engineered): \"{one_shot_refinement}\""
            )
        },
        {
            "role": "user",
            "content": (
                f"Original prompt (Zero-shot): \"{non_optimized_prompt}\"\n"
                f"Refined prompt (Human-Engineered):"
            )
        }
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.3
    )

    return response["choices"][0]["message"]["content"].strip(' "')