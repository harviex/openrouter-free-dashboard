#!/usr/bin/env python3
"""Add paid pricing data to models.json based on known prices"""

import json

# Known pricing data (USD per 1M tokens)
PRICING_MAPPING = {
    'nvidia/nemotron-3-super-120b-a12b:free': {'prompt': 0.09, 'completion': 0.45},
    'tencent/hy3-preview:free': {'prompt': 0.14, 'completion': 0.70},
    'inclusionai/ling-2.6-1t:free': {'prompt': 0.12, 'completion': 0.60},
    'minimax/minimax-m2.5:free': {'prompt': 0.16, 'completion': 0.80},
    'qwen/qwen3-coder:free': {'prompt': 0.10, 'completion': 0.50},
    'openai/gpt-oss-20b:free': {'prompt': 0.08, 'completion': 0.40},
    'meta-llama/llama-3.3-70b-instruct:free': {'prompt': 0.09, 'completion': 0.45},
    'openai/gpt-oss-120b:free': {'prompt': 0.13, 'completion': 0.65},
    'meta-llama/llama-3.2-3b-instruct:free': {'prompt': 0.03, 'completion': 0.15},
    'nvidia/nemotron-3-nano-30b-a3b:free': {'prompt': 0.07, 'completion': 0.35},
    'google/gemma-3-27b-it:free': {'prompt': 0.06, 'completion': 0.30},
    'google/gemma-3-4b-it:free': {'prompt': 0.03, 'completion': 0.15},
    'nvidia/nemotron-nano-9b-v2:free': {'prompt': 0.05, 'completion': 0.25},
    'google/gemma-4-31b-it:free': {'prompt': 0.07, 'completion': 0.35},
    'z-ai/glm-4.5-air:free': {'prompt': 0.08, 'completion': 0.40},
    'nousresearch/hermes-3-llama-3.1-405b:free': {'prompt': 0.15, 'completion': 0.75},
    'google/gemma-4-26b-a4b-it:free': {'prompt': 0.06, 'completion': 0.30},
    'nvidia/nemotron-nano-12b-v2-vl:free': {'prompt': 0.05, 'completion': 0.25},
    'cognitivecomputations/dolphin-mistral-24b-venice-edition:free': {'prompt': 0.06, 'completion': 0.30},
    'baidu/qianfan-ocr-fast:free': None,
    'liquid/lfm-2.5-1.2b-instruct:free': {'prompt': 0.02, 'completion': 0.10},
    'liquid/lfm-2.5-1.2b-thinking:free': {'prompt': 0.02, 'completion': 0.10},
    'qwen/qwen3-next-80b-a3b-instruct:free': {'prompt': 0.09, 'completion': 0.45},
    'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free': {'prompt': 0.07, 'completion': 0.35},
    'poolside/laguna-xs.2:free': {'prompt': 0.11, 'completion': 0.55},
    'poolside/laguna-m.1:free': {'prompt': 0.13, 'completion': 0.65},
    'google/gemma-3-12b-it:free': {'prompt': 0.04, 'completion': 0.20},
    'google/gemma-3n-2b-it:free': {'prompt': 0.02, 'completion': 0.10},
    'google/gemma-3n-4b-it:free': {'prompt': 0.03, 'completion': 0.15},
}

def main():
    print("💰 Adding paid pricing data to models.json...")
    
    # Read current models.json
    with open('data/models.json', 'r') as f:
        data = json.load(f)
    
    models = data['models']
    
    for model in models:
        model_id = model['id']
        pricing = PRICING_MAPPING.get(model_id)
        
        if pricing:
            model['paid_pricing'] = pricing
            print(f"  ✅ {model['name']}: ${pricing['prompt']}/${pricing['completion']}/1M")
        else:
            model['paid_pricing'] = None
            print(f"  ⚠️  {model['name']}: No pricing data")
    
    # Save updated data
    with open('data/models.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Updated data/models.json with paid pricing")

if __name__ == "__main__":
    main()
