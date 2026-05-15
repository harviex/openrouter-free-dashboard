#!/usr/bin/env python3
"""Add parameters field back to models.json based on model names and HF data"""

import json
import urllib.request
import time

# Model ID to parameters mapping (based on model names)
PARAM_MAPPING = {
    "nvidia/nemotron-3-super-120b-a12b:free": "120B",
    "tencent/hy3-preview:free": "295B",
    "inclusionai/ring-2.6-1t:free": "1T-A63B",
    "inclusionai/ling-2.6-1t:free": "1T",
    "inclusionai/ling-2.6-flash:free": "1T",
    "minimax/minimax-m2.5:free": "230B-A10B",
    "qwen/qwen3-coder:free": "480B",
    "openai/gpt-oss-20b:free": "20B",
    "meta-llama/llama-3.3-70b-instruct:free": "70B",
    "openai/gpt-oss-120b:free": "120B",
    "meta-llama/llama-3.2-3b-instruct:free": "3B",
    "nvidia/nemotron-3-nano-30b-a3b:free": "30B",
    "google/gemma-3-27b-it:free": "27B",
    "google/gemma-3-4b-it:free": "4B",
    "nvidia/nemotron-nano-9b-v2:free": "9B",
    "google/gemma-4-31b-it:free": "31B",
    "z-ai/glm-4.5-air:free": "106B-A12B",
    "nousresearch/hermes-3-llama-3.1-405b:free": "405B",
    "google/gemma-4-26b-a4b-it:free": "26B",
    "nvidia/nemotron-nano-12b-v2-vl:free": "12B",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free": "30B",
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free": "24B",
    "baidu/qianfan-ocr-fast:free": "Unknown",
    "baidu/cobuddy:free": "28B-A3B",
    "liquid/lfm-2.5-1.2b-instruct:free": "1.2B",
    "liquid/lfm-2.5-1.2b-thinking:free": "1.2B",
    "qwen/qwen3-next-80b-a3b-instruct:free": "80B",
    "poolside/laguna-xs.2:free": "33B-A3B",
    "poolside/laguna-m.1:free": "225B-A23B",
    "deepseek/deepseek-v4-flash:free": "284B-A13B",
    "google/gemma-3-12b-it:free": "12B",
    "google/gemma-3n-e2b-it:free": "2B",
    "google/gemma-3n-e4b-it:free": "4B",
    "openrouter/free": "Unknown",
}

def main():
    print("📊 Adding parameters field to models.json...")

    # Read current models.json
    with open('data/models.json', 'r') as f:
        data = json.load(f)

    models = data['models']

    for model in models:
        model_id = model['id']
        # Add parameters field
        params = PARAM_MAPPING.get(model_id, "Unknown")
        model['parameters'] = params
        print(f"  ✅ {model['name']}: {params}")

    # Save updated data
    with open('data/models.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n✅ Updated data/models.json with parameters field")

if __name__ == "__main__":
    main()