#!/usr/bin/env python3
"""
Update OpenRouter Free Models Dashboard with HuggingFace scores
- Fetches HuggingFace data for each model using standard library
- Calculates total score (popularity 40% + freshness 20% + benchmark 40%)
- Updates data/models.json with scores
"""

import json
import urllib.request
import urllib.error
import time
from datetime import datetime
import math
import os

# HuggingFace API token from environment variable
HF_TOKEN = os.environ.get('HF_TOKEN', '')
if not HF_TOKEN:
    print("⚠️  Warning: HF_TOKEN environment variable not set")
    print("   HuggingFace data will not be fetched")
    print("   Scores will use default values")

# OpenRouter model ID to HuggingFace model ID mapping
HF_MAPPING = {
    "nvidia/nemotron-3-super-120b-a12b:free": "nvidia/Nemotron-3-Super-120B-A12B",
    "tencent/hy3-preview:free": "tencent/Hy3-preview",
    "inclusionai/ling-2.6-1t:free": "inclusionAI/Ling-2.6-1T",
    "minimax/minimax-m2.5:free": "MiniMax/MiniMax-M2.5",
    "qwen/qwen3-coder:free": "Qwen/Qwen3-Coder-480B-A35B",
    "openai/gpt-oss-20b:free": "openai/gpt-oss-20b",
    "meta-llama/llama-3.3-70b-instruct:free": "meta-llama/Llama-3.3-70B-Instruct",
    "openai/gpt-oss-120b:free": "openai/gpt-oss-120b",
    "meta-llama/llama-3.2-3b-instruct:free": "meta-llama/Llama-3.2-3B-Instruct",
    "nvidia/nemotron-3-nano-30b-a3b:free": "nvidia/Nemotron-3-Nano-30B-A3B",
    "google/gemma-3-27b-it:free": "google/gemma-3-27b-it",
    "google/gemma-3-4b-it:free": "google/gemma-3-4b-it",
    "nvidia/nemotron-nano-9b-v2:free": "nvidia/Nemotron-Nano-9B-v2",
    "google/gemma-4-31b-it:free": None,
    "z-ai/glm-4.5-air:free": "zai-org/GLM-4.5-Air",
    "nousresearch/hermes-3-llama-3.1-405b:free": "NousResearch/Hermes-3-Llama-3.1-405B",
    "google/gemma-4-26b-a4b-it:free": None,
    "nvidia/nemotron-nano-12b-v2-vl:free": "nvidia/Nemotron-Nano-12B-v2-VL",
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free": "cognitivecomputations/Dolphin-Mistral-24B-Venice-Edition",
    "baidu/qianfan-ocr-fast:free": None,
    "liquid/lfm-2.5-1.2b-instruct:free": "LiquidAI/LFM2.5-1.2B-Instruct",
    "liquid/lfm-2.5-1.2b-thinking:free": "LiquidAI/LFM2.5-1.2B-Thinking",
    "qwen/qwen3-next-80b-a3b-instruct:free": "Qwen/Qwen3-Next-80B-A3B-Instruct",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free": "nvidia/Nemotron-3-Nano-Omni-30B-A3B",
    "poolside/laguna-xs.2:free": "Poolside/Laguna-XS.2",
    "poolside/laguna-m.1:free": "Poolside/Laguna-M.1",
    "google/gemma-3-12b-it:free": "google/gemma-3-12b-it",
    "google/gemma-3n-e2b-it:free": "google/gemma-3n-2b-it",
    "google/gemma-3n-e4b-it:free": "google/gemma-3n-4b-it",
}

def get_hf_data(hf_model_id):
    """Fetch model data from HuggingFace API using standard library"""
    if not hf_model_id:
        return None
    
    url = f"https://huggingface.co/api/models/{hf_model_id}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.HTTPError as e:
        print(f"  ⚠️  HTTP Error {e.code} for {hf_model_id}")
        return None
    except Exception as e:
        print(f"  ⚠️  Error fetching {hf_model_id}: {e}")
        return None

def calculate_score(hf_data, created_timestamp):
    """Calculate total score based on the formula"""
    if not hf_data:
        return 3.0
    
    # 1. Popularity score (40%)
    likes = hf_data.get('likes', 0)
    downloads = hf_data.get('downloads', 0)
    
    likes_norm = min(math.log10(max(likes, 1)) / 3.5, 1.0)
    downloads_norm = min(math.log10(max(downloads, 1)) / 6.0, 1.0)
    
    popularity_score = (likes_norm * 0.3 + downloads_norm * 0.7) * 5.0
    
    # 2. Freshness score (20%)
    created_dt = datetime.fromtimestamp(created_timestamp)
    days_since_created = (datetime.now() - created_dt).days
    freshness_score = max(0, (1 - days_since_created / 365)) * 5.0
    
    # 3. Benchmark score (40%)
    tags = hf_data.get('tags', [])
    has_eval = 'eval-results' in tags
    
    benchmark_score = 3.5 if has_eval else 3.0
    if has_eval and ('mmlu' in str(tags).lower() or 'MMLU' in str(hf_data)):
        benchmark_score += 0.5
    
    # Total score
    total_score = popularity_score * 0.4 + freshness_score * 0.2 + benchmark_score * 0.4
    total_score = max(0.0, min(5.0, total_score))
    
    return round(total_score, 1)

def main():
    print("🚀 Starting update process...")
    
    # Read current models.json
    with open('data/models.json', 'r') as f:
        data = json.load(f)
    
    models = data['models']
    print(f"📊 Processing {len(models)} models...")
    
    hf_data_cache = {}
    
    # First pass: collect HF data
    for model in models:
        model_id = model['id']
        hf_id = HF_MAPPING.get(model_id)
        
        print(f"\n🔍 Processing: {model['name']}")
        print(f"   HF ID: {hf_id}")
        
        if hf_id:
            hf_data = get_hf_data(hf_id)
            hf_data_cache[model_id] = hf_data
            if hf_data:
                likes = hf_data.get('likes', 0)
                downloads = hf_data.get('downloads', 0)
                print(f"   ✅ Likes: {likes}, Downloads: {downloads}")
            time.sleep(0.3)
        else:
            print(f"   ⚠️  No HF mapping available")
            hf_data_cache[model_id] = None
    
    # Second pass: calculate scores
    print("\n📈 Calculating scores...")
    for model in models:
        model_id = model['id']
        hf_data = hf_data_cache.get(model_id)
        
        score = calculate_score(hf_data, model.get('created', 0))
        model['score'] = score
        
        print(f"   ⭐ {model['name']}: {score}/5.0")
    
    # Save updated data
    with open('data/models.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Updated data/models.json")
    print("\n⚠️  Next steps:")
    print("1. Update script.js to display score instead of parameters")
    print("2. Test locally")
    print("3. Commit and push to GitHub")

if __name__ == "__main__":
    main()
