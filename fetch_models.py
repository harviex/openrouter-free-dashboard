#!/usr/bin/env python3
"""
Fetch free models from OpenRouter website (authoritative) and enrich with API data.
Website: https://openrouter.ai/collections/free-models
API: https://openrouter.ai/api/v1/models
"""
import json
import subprocess
import os
import re
from datetime import datetime, timedelta

# Manual parameter mapping for models where API doesn't provide parameters
PARAMETER_MAP = {
    'tencent/hy3-preview:free': '295B',
    'tencent/hy3-preview': '295B',
    'qwen/qwen3-coder:free': '480B',
    'openai/gpt-oss-120b:free': '120B',
    'openai/gpt-oss-20b:free': '20B',
    'nvidia/nemotron-3-super-120b-a12b:free': '120B',
    'nvidia/nemotron-3-nano-30b-a3b:free': '30B',
    'meta-llama/llama-3.3-70b-instruct:free': '70B',
    'meta-llama/llama-3.2-3b-instruct:free': '3B',
    'google/gemma-3-27b-it:free': '27B',
    'google/gemma-3-4b-it:free': '4B',
    'google/gemma-4-31b-it:free': '31B',
    'google/gemma-4-26b-a4b-it:free': '26B',
    'nvidia/nemotron-nano-9b-v2:free': '9B',
    'nvidia/nemotron-nano-12b-v2-vl:free': '12B',
    'z-ai/glm-4.5-air:free': '45B',
    'nousresearch/hermes-3-llama-3.1-405b:free': '405B',
    'minimax/minimax-m2.5:free': '35B',
    'inclusionai/ring-2.6-1t:free': '1T',
    'inclusionai/ling-2.6-1t:free': '1T',
    'inclusionai/ling-2.6-flash:free': '1T',
    'arcee-ai/trinity-large-thinking:free': '398B',
    'baidu/cobuddy:free': 'Unknown',
    'liquid/lfm-2.5-1.2b-thinking:free': '1.2B',
    'liquid/lfm-2.5-1.2b-instruct:free': '1.2B',
    'cognitivecomputations/dolphin-mistral-24b-venice-edition:free': '24B',
    'baidu/qianfan-ocr-fast:free': '4B',
    'poolside/laguna-xs.2:free': '33B-A3B',
    'poolside/laguna-m.1:free': '225B-A23B',
    'deepseek/deepseek-v4-flash:free': '284B-A13B',
    'openrouter/free': 'Unknown',
    # New models from website
    'perplexity/pplx-decider-v1.3:free': 'Unknown',
    'perplexity/pplx-decider-flash-v1.3:free': 'Unknown',
    'respan/span-01-lite': 'Unknown',
    'nvidia/llama-nemotron-rerank-vl-1b-v2:free': '1B',
    'nvidia/nemotron-3.5-rerank-8b:free': '8B',
    'nvidia/nemotron-3-embed-1b:free': '1B',
    'nvidia/nemotron-3.5-embed-8b:free': '8B',
    'nvidia/llama-nemotron-embed-vl-1b-v2:free': '1B',
    'stealth/crouton-alpha': 'Unknown',
    'xingchen-agi/xing4.0-29b-a4b:free': '29B-A4B',
    'poolside/laguna-s-2.1:free': 'Unknown',
    'poolside/laguna-xs-2.1:free': 'Unknown',
    'qwen/qwen3.8-27b:free': '27B',
    'inclusionai/ling-3.0-flash-sante:free': 'Unknown',
    'inclusionai/ling-3.1-flash': 'Unknown',
    'apodex/apodex-1.1-mini:free': 'Unknown',
}

# Usage volume data (in billions of tokens, from OpenRouter free-models page)
USAGE_DATA = {
    'nvidia/nemotron-3-super-120b-a12b:free': 677,
    'tencent/hy3-preview:free': 638,
    'inclusionai/ling-2.6-1t:free': 369,
    'inclusionai/ling-2.6-flash:free': 208,
    'minimax/minimax-m2.5:free': 97.7,
    'qwen/qwen3-coder:free': 94.2,
    'google/gemma-4-31b-it:free': 16.1,
    'google/gemma-4-26b-a4b-it:free': 9.26,
    'meta-llama/llama-3.3-70b-instruct:free': 45.2,
    'openai/gpt-oss-120b:free': 38.5,
    'openai/gpt-oss-20b:free': 52.3,
    'nvidia/nemotron-3-nano-30b-a3b:free': 28.7,
    'z-ai/glm-4.5-air:free': 15.8,
    'google/gemma-3-27b-it:free': 22.4,
    'meta-llama/llama-3.2-3b-instruct:free': 35.6,
    'nousresearch/hermes-3-llama-3.1-405b:free': 12.3,
    'nvidia/nemotron-nano-12b-v2-vl:free': 8.9,
    'nvidia/nemotron-nano-9b-v2:free': 18.7,
    'baidu/qianfan-ocr-fast:free': 5.2,
    'liquid/lfm-2.5-1.2b-thinking:free': 3.8,
    'liquid/lfm-2.5-1.2b-instruct:free': 4.5,
    'cognitivecomputations/dolphin-mistral-24b-venice-edition:free': 7.6,
    'google/gemma-3-4b-it:free': 19.3,
    'openrouter/free': 156.7,
    # Website usage data (tokens/wk from free-models page, converted to billions)
    'nvidia/nemotron-3-ultra-550b-a55b:free': 3310,  # 3.31T
    'nvidia/nemotron-3.5-super-vl:free': 3060,  # 3.06T
    'baidu/ernie-5.5-flash-preview:free': 1540,  # 1.54T
    'nvidia/nemotron-3.5-lightning:free': 1160,  # 1.16T
    'thinkingmachines/inkling-2-small:free': 932,
    'dots-studio/dots-3-note-preview:free': 743,
    'particle-ai/particle-1:free': 225,
    'cohere/north-mini-code:free': 196,
    'recursive/flint-v1.0:free': 149,
    'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free': 102,
    'perplexity/pplx-decider-v1.3:free': 72.3,
    'inclusionai/ling-3.2-flash:free': 7.3,
    'liquid/lfm-3-1.7b:free': 37.9,
    'perplexity/pplx-decider-flash-v1.3:free': 3.9,
    'respan/span-01-lite': 4.91,
    'nvidia/llama-nemotron-rerank-vl-1b-v2:free': 1.59,
}

def fetch_website_free_models():
    """Scrape the free-models collection page for authoritative model list"""
    url = "https://openrouter.ai/collections/free-models"
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--connect-timeout', '30', '--max-time', '60',
             '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
             url],
            capture_output=True, text=True, timeout=90
        )
        if result.returncode != 0:
            print(f"curl error: {result.stderr.strip()}")
            return []
        html = result.stdout
        
        # Extract all :free model IDs directly from HTML (they appear in JSON data, links, etc.)
        # Pattern: provider/model-name:free (with optional date suffix)
        free_models_raw = re.findall(r'([a-z0-9-]+/[a-z0-9.-]+:free)', html)
        
        # Normalize: remove date suffixes like -20261113, keep base model ID
        normalized = set()
        for m in free_models_raw:
            # Remove trailing date pattern like -20261113
            base = re.sub(r'-\d{8}$', '', m)
            normalized.add(base)
        
        free_models = sorted(normalized)
        
        print(f"Website free models found: {len(free_models)}")
        for m in free_models:
            print(f"  {m}")
        return free_models
    except Exception as e:
        print(f"Error fetching website: {e}")
        return []

def fetch_api_models():
    """Fetch all models from OpenRouter API"""
    url = "https://openrouter.ai/api/v1/models"
    try:
        result = subprocess.run(
            ['curl', '-s', '--connect-timeout', '30', '--max-time', '60',
             '-H', 'User-Agent: Mozilla/5.0', url],
            capture_output=True, text=True, timeout=90
        )
        if result.returncode != 0:
            print(f"curl error: {result.stderr.strip()}")
            return []
        data = json.loads(result.stdout)
        return data.get('data', [])
    except Exception as e:
        print(f"Error fetching API: {e}")
        return []

def is_free_model(model):
    """Check if a model is free (prompt and completion are 0)"""
    pricing = model.get('pricing', {})
    try:
        prompt_price = float(pricing.get('prompt', '0'))
        completion_price = float(pricing.get('completion', '0'))
        return prompt_price == 0 and completion_price == 0
    except:
        return False

def extract_model_info(model, last_updated=None):
    """Extract relevant information from model data"""
    architecture = model.get('architecture', {})
    input_modalities = architecture.get('input_modalities', [])
    output_modalities = architecture.get('output_modalities', [])
    
    has_tools = 'tools' in model.get('supported_parameters', [])
    has_vision = 'image' in input_modalities
    has_reasoning = 'include_reasoning' in model.get('supported_parameters', [])
    
    model_id = model.get('id', '')
    provider = model_id.split('/')[0] if '/' in model_id else 'Unknown'
    provider = provider.replace('-', ' ').title()
    
    model_name = model.get('name', '')
    parameters = extract_parameters(model_name, model_id)
    
    paid_pricing = get_paid_pricing(model_id)
    
    expiration = model.get('expiration_date', None)
    
    usage_volume = USAGE_DATA.get(model_id, None)
    usage_display = None
    if usage_volume:
        if usage_volume >= 1000:
            usage_display = f"{usage_volume/1000:.1f}T"
        elif usage_volume >= 1:
            usage_display = f"{usage_volume:.1f}B"
        else:
            usage_display = f"{usage_volume*1000:.0f}M"
    
    requests_per_day = None
    if last_updated:
        analytics_by_date = extract_analytics(model_id)
        if analytics_by_date:
            target_date = (last_updated - timedelta(days=1)).strftime('%Y-%m-%d')
            entry = analytics_by_date.get(target_date)
            if entry:
                requests_per_day = entry.get('count')
    
    return {
        'id': model_id,
        'name': model.get('name', 'Unknown Model'),
        'provider': provider,
        'context_length': model.get('context_length', 0),
        'parameters': parameters,
        'has_tools': has_tools,
        'has_vision': has_vision,
        'has_reasoning': has_reasoning,
        'pricing_prompt': float(model.get('pricing', {}).get('prompt', '0')),
        'pricing_completion': float(model.get('pricing', {}).get('completion', '0')),
        'paid_pricing': paid_pricing,
        'created': model.get('created', 0),
        'description': model.get('description', ''),
        'supported_parameters': model.get('supported_parameters', []),
        'expiration_date': expiration,
        'model_url': f"https://openrouter.ai/{model_id}",
        'usage_volume': usage_display,
        'usage_raw': usage_volume,
        'requests_per_day': requests_per_day
    }

def get_paid_pricing(free_model_id):
    """Get pricing from the non-free version of the model"""
    if free_model_id.endswith(':free'):
        paid_model_id = free_model_id[:-5]
    else:
        return None
    url = f"https://openrouter.ai/api/v1/models/{paid_model_id}"
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--connect-timeout', '15',
             '-H', 'User-Agent: Mozilla/5.0', url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        model_data = data.get('data', {})
        if isinstance(model_data, list):
            if len(model_data) > 0:
                model_data = model_data[0]
            else:
                return None
        pricing = model_data.get('pricing', {})
        prompt_per_token = float(pricing.get('prompt', '0'))
        completion_per_token = float(pricing.get('completion', '0'))
        if prompt_per_token == 0 and completion_per_token == 0:
            return None
        prompt_per_1m = round(prompt_per_token * 1000000, 6)
        completion_per_1m = round(completion_per_token * 1000000, 6)
        return {'prompt': prompt_per_1m, 'completion': completion_per_1m}
    except:
        return None

def extract_analytics(model_id):
    """Extract analytics data from model page"""
    page_path = model_id.replace(':free', '')
    url = f"https://openrouter.ai/{page_path}"
    try:
        cmd = [
            'curl', '-s', '-L',
            '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            '-H', 'Accept-Language: en-US,en;q=0.5',
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        html = result.stdout
        if not html:
            return None
        match = re.search(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if not match:
            return None
        data = json.loads(match.group(1))
        page_props = data.get('props', {}).get('pageProps', {})
        model_data = page_props.get('model', {})
        analytics = model_data.get('analytics', [])
        if not analytics:
            return None
        analytics_by_date = {}
        for entry in analytics:
            date_str = entry.get('date', '')
            if date_str:
                date_only = date_str.split()[0] if ' ' in date_str else date_str
                analytics_by_date[date_only] = entry
        return analytics_by_date
    except Exception as e:
        return None

def extract_parameters(model_name, model_id):
    """Extract parameter count from model name or id"""
    if model_id in PARAMETER_MAP:
        return PARAMETER_MAP[model_id]
    import re
    text = (model_name + ' ' + model_id).lower()
    matches = re.findall(r'(\d+(?:\.\d+)?)\s*b', text)
    if matches:
        params = sorted(matches, key=lambda x: float(x), reverse=True)
        return f"{params[0]}B"
    moe_matches = re.findall(r'a(\d+(?:\.\d+)?)\s*b', text)
    if moe_matches:
        params = sorted(moe_matches, key=lambda x: float(x), reverse=True)
        return f"A{params[0]}B"
    return None

def calculate_score(model_info, all_models):
    """Calculate a score from 0-5 based on usage volume"""
    usage = model_info.get('usage_raw', 0)
    if not usage:
        return None
    all_usages = [m.get('usage_raw', 0) for m in all_models if m.get('usage_raw')]
    if not all_usages:
        return None
    max_usage = max(all_usages)
    min_usage = min(all_usages)
    if max_usage == min_usage:
        return 2.5
    normalized = (usage - min_usage) / (max_usage - min_usage)
    score = round(normalized * 5, 1)
    if model_info.get('has_tools'): score += 0.2
    if model_info.get('has_vision'): score += 0.1
    if model_info.get('has_reasoning'): score += 0.1
    return min(round(score, 1), 5.0)

def main():
    print("=" * 60)
    print("Fetching OpenRouter Free Models (Website + API)")
    print("=" * 60)
    
    # 1. Get authoritative model list from website
    print("\n>>> Step 1: Scraping website free-models page...")
    website_model_ids = fetch_website_free_models()
    
    # Add known models that might not be on the ranked page
    known_extra = [
        'google/gemma-4-31b-it:free',
        'google/gemma-4-26b-a4b-it:free',
        'google/lyria-3-pro-preview',
        'google/lyria-3-clip-preview',
        'openrouter/free',
        'respan/span-01-lite',  # no :free suffix but shown as free on website
    ]
    for m in known_extra:
        if m not in website_model_ids:
            website_model_ids.append(m)
    
    # Normalize and deduplicate by base model ID (remove date suffixes)
    # Priority: non-dated version > dated version
    def normalize_model_id(mid):
        # Remove date suffix like -20260604 (followed by :free or end of string)
        return re.sub(r'-\d{8}(?=:free|$)', '', mid)
    
    # First pass: collect all base (non-dated) versions
    base_versions = set()
    for mid in website_model_ids:
        if not re.search(r'-\d{8}(?=:free|$)', mid):
            base_versions.add(mid)
    
    # Second pass: for dated versions, only keep if no base version exists
    normalized_to_original = {}
    # Add base versions first (highest priority)
    for mid in base_versions:
        normalized_to_original[mid] = mid
    
    # Add dated versions only if base doesn't exist
    for mid in website_model_ids:
        if re.search(r'-\d{8}(?=:free|$)', mid):
            norm = normalize_model_id(mid)
            if norm not in normalized_to_original:
                normalized_to_original[norm] = mid
    
    # Use normalized model IDs as authoritative list
    final_model_ids = list(normalized_to_original.keys())
    
    print(f"Total website model IDs (deduplicated): {len(final_model_ids)}")
    for m in final_model_ids:
        print(f"  {m}")
    
    # 2. Fetch API models for enrichment
    print("\n>>> Step 2: Fetching API models for enrichment...")
    api_models = fetch_api_models()
    api_by_id = {m.get('id', ''): m for m in api_models}
    print(f"API models fetched: {len(api_models)}")
    
    # 3. Build final model list: website IDs as primary, enriched with API data
    print("\n>>> Step 3: Building final model list...")
    last_updated = datetime.now()
    final_models = []
    
    for model_id in final_model_ids:
        api_model = api_by_id.get(model_id)
        if api_model:
            # Enrich with API data
            model_info = extract_model_info(api_model, last_updated)
            model_info['source'] = 'api'
        else:
            # Model not in API - create minimal entry with manual data
            print(f"  WARNING: {model_id} not in API, using manual data")
            model_info = {
                'id': model_id,
                'name': model_id.split('/')[-1].replace('-', ' ').replace(':free', '').title(),
                'provider': model_id.split('/')[0].replace('-', ' ').title() if '/' in model_id else 'Unknown',
                'context_length': 0,
                'parameters': PARAMETER_MAP.get(model_id, 'Unknown'),
                'has_tools': False,
                'has_vision': False,
                'has_reasoning': False,
                'pricing_prompt': 0.0,
                'pricing_completion': 0.0,
                'paid_pricing': None,
                'created': 0,
                'description': '',
                'supported_parameters': [],
                'expiration_date': None,
                'model_url': f"https://openrouter.ai/{model_id}",
                'usage_volume': None,
                'usage_raw': USAGE_DATA.get(model_id),
                'requests_per_day': None,
                'source': 'manual'
            }
            # Try to get usage volume from our data
            if model_id in USAGE_DATA:
                uv = USAGE_DATA[model_id]
                if uv >= 1000:
                    model_info['usage_volume'] = f"{uv/1000:.1f}T"
                elif uv >= 1:
                    model_info['usage_volume'] = f"{uv:.1f}B"
                else:
                    model_info['usage_volume'] = f"{uv*1000:.0f}M"
        
        final_models.append(model_info)
    
    # 4. Calculate scores
    print("\n>>> Step 4: Calculating scores...")
    for model in final_models:
        score = calculate_score(model, final_models)
        if score is not None:
            model['score'] = score
    
    # 5. Sort by usage volume (descending)
    final_models.sort(key=lambda x: (x['usage_raw'] or 0, x['context_length']), reverse=True)
    
    # 6. Get unique providers
    providers = sorted(set(m['provider'] for m in final_models))
    
    # 7. Prepare output
    output = {
        'last_updated': last_updated.strftime('%Y-%m-%d %H:%M:%S UTC'),
        'total_models': len(final_models),
        'total_providers': len(providers),
        'providers': providers,
        'models': final_models
    }
    
    # 8. Write to file
    with open('data/models.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nData written to data/models.json")
    print(f"Models: {len(final_models)}, Providers: {len(providers)}")
    print("\nAll models:")
    for m in final_models:
        src = m.get('source', 'unknown')
        print(f"  {m['id']} [{src}] - {m['name']} - usage: {m['usage_volume'] or 'N/A'}")

if __name__ == '__main__':
    main()
