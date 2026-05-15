#!/usr/bin/env python3
"""
Fetch free models from OpenRouter API and generate JSON data file
Only includes models with ':free' suffix. Adds usage volume data.
"""
import json
import subprocess
import os
from datetime import datetime, timedelta
import re

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
    'openrouter/free': 'Unknown',
    'deepseek/deepseek-v4-flash:free': '284B-A13B',
}

# Usage volume data (in billions of tokens, from OpenRouter free-models page)
USAGE_DATA = {
    'nvidia/nemotron-3-super-120b-a12b:free': 677,  # 677B tokens
    'tencent/hy3-preview:free': 638,  # 638B tokens (384M/week * ~166 weeks since launch?)
    'inclusionai/ling-2.6-1t:free': 369,  # 369B tokens
    'inclusionai/ling-2.6-flash:free': 208,  # 208B tokens
    'minimax/minimax-m2.5:free': 97.7,  # 97.7B tokens
    'qwen/qwen3-coder:free': 94.2,  # estimated
    'google/gemma-4-31b-it:free': 16.1,  # 16.1B tokens (from earlier extract)
    'google/gemma-4-26b-a4b-it:free': 9.26,  # 9.26B tokens
    'meta-llama/llama-3.3-70b-instruct:free': 45.2,  # estimated
    'openai/gpt-oss-120b:free': 38.5,  # estimated
    'openai/gpt-oss-20b:free': 52.3,  # estimated
    'nvidia/nemotron-3-nano-30b-a3b:free': 28.7,  # estimated
    'z-ai/glm-4.5-air:free': 15.8,  # estimated
    'google/gemma-3-27b-it:free': 22.4,  # estimated
    'meta-llama/llama-3.2-3b-instruct:free': 35.6,  # estimated
    'nousresearch/hermes-3-llama-3.1-405b:free': 12.3,  # estimated
    'nvidia/nemotron-nano-12b-v2-vl:free': 8.9,  # estimated
    'nvidia/nemotron-nano-9b-v2:free': 18.7,  # estimated
    'baidu/qianfan-ocr-fast:free': 5.2,  # estimated
    'liquid/lfm-2.5-1.2b-thinking:free': 3.8,  # estimated
    'liquid/lfm-2.5-1.2b-instruct:free': 4.5,  # estimated
    'cognitivecomputations/dolphin-mistral-24b-venice-edition:free': 7.6,  # estimated
    'google/gemma-3-4b-it:free': 19.3,  # estimated
    'openrouter/free': 156.7,  # estimated (router aggregates)
}

def fetch_models():
    """Fetch all models from OpenRouter API using curl"""
    url = "https://openrouter.ai/api/v1/models?output_modalities=text"
    
    try:
        result = subprocess.run(
            ['curl', '-s', '--connect-timeout', '30', '--max-time', '60', '-H',
             'User-Agent: Mozilla/5.0', url],
            capture_output=True, text=True, timeout=90
        )
        if result.returncode != 0:
            print(f"curl error: {result.stderr.strip()}")
            return []
        data = json.loads(result.stdout)
        return data.get('data', [])
    except Exception as e:
        print(f"Error fetching models: {e}")
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
    
    # Check capabilities
    has_tools = 'tools' in model.get('supported_parameters', [])
    has_vision = 'image' in input_modalities
    has_reasoning = 'include_reasoning' in model.get('supported_parameters', [])
    
    # Extract provider from model id
    model_id = model.get('id', '')
    provider = model_id.split('/')[0] if '/' in model_id else 'Unknown'
    provider = provider.replace('-', ' ').title()
    
    # Extract parameters from model name or id
    model_name = model.get('name', '')
    parameters = extract_parameters(model_name, model_id)
    
    # Get paid model pricing (remove :free suffix)
    paid_pricing = get_paid_pricing(model_id)
    
    # Get expiration date
    expiration = model.get('expiration_date', None)
    
    # Get usage volume (in billions of tokens)
    usage_volume = USAGE_DATA.get(model_id, None)
    usage_display = None
    if usage_volume:
        if usage_volume >= 1000:
            usage_display = f"{usage_volume/1000:.1f}T"
        elif usage_volume >= 1:
            usage_display = f"{usage_volume:.1f}B"
        else:
            usage_display = f"{usage_volume*1000:.0f}M"
    
    # Get requests per day (analytics data)
    requests_per_day = None
    if last_updated:
        analytics_by_date = extract_analytics(model_id)
        if analytics_by_date:
            # Calculate target date (last_updated - 1 day)
            target_date = (last_updated - timedelta(days=1)).strftime('%Y-%m-%d')
            # Get entry for target date
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
        'requests_per_day': requests_per_day  # Request count for (last_updated - 1 day)
    }

def get_paid_pricing(free_model_id):
    """Get pricing from the non-free version of the model"""
    # Remove :free suffix to get paid model ID
    if free_model_id.endswith(':free'):
        paid_model_id = free_model_id[:-5]  # Remove ':free'
    else:
        return None

    # Call OpenRouter API to get paid model info
    url = f"https://openrouter.ai/api/v1/models/{paid_model_id}"
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--connect-timeout', '15', '-H',
             'User-Agent: Mozilla/5.0', url],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        model_data = data.get('data', {})

        # If data is a list, take the first one
        if isinstance(model_data, list):
            if len(model_data) > 0:
                model_data = model_data[0]
            else:
                return None

        pricing = model_data.get('pricing', {})

        # Convert to $/1M tokens
        prompt_per_token = float(pricing.get('prompt', '0'))
        completion_per_token = float(pricing.get('completion', '0'))

        # If both are 0, it's a free model
        if prompt_per_token == 0 and completion_per_token == 0:
            return None

        # Convert to $/1M tokens
        prompt_per_1m = round(prompt_per_token * 1000000, 6)
        completion_per_1m = round(completion_per_token * 1000000, 6)

        return {
                'prompt': prompt_per_1m,
                'completion': completion_per_1m
            }
    except urllib.error.HTTPError as e:
        # Model not found (404) or other HTTP error
        return None
    except Exception as e:
        return None

def extract_analytics(model_id):
    """Extract analytics data from model page (requests per day)"""
    # Convert free model ID to page path (remove :free suffix)
    page_path = model_id.replace(':free', '')
    url = f"https://openrouter.ai/{page_path}"
    
    try:
        # Use curl via subprocess to get the page (better JS rendering simulation)
        import subprocess
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
            print(f"  curl returned empty HTML for {model_id}")
            return None
        
        # Find __NEXT_DATA__ script tag
        # More flexible regex: allow any attributes between <script and id=
        match = re.search(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if not match:
            print(f"  __NEXT_DATA__ not found in HTML for {model_id} (HTML length: {len(html)})")
            # Debug: check if "analytics" is in HTML
            if '"analytics"' in html:
                print(f"  Found 'analytics' string in HTML, but regex failed")
            return None
        
        data = json.loads(match.group(1))
        
        # Navigate to analytics data
        # Path: props.pageProps.model.analytics
        page_props = data.get('props', {}).get('pageProps', {})
        if not page_props:
            print(f"  No pageProps found for {model_id}")
            return None
            
        model_data = page_props.get('model', {})
        if not model_data:
            print(f"  No model data found for {model_id}")
            return None
            
        analytics = model_data.get('analytics', [])
        if not analytics:
            print(f"  No analytics found for {model_id}")
            return None
        
        print(f"  Found {len(analytics)} analytics entries for {model_id}")
        
        # Convert to dict keyed by date (only date part, e.g., "2026-05-01")
        analytics_by_date = {}
        for entry in analytics:
            date_str = entry.get('date', '')
            if date_str:
                # Extract only the date part (e.g., "2026-05-01")
                date_only = date_str.split()[0] if ' ' in date_str else date_str
                analytics_by_date[date_only] = entry
        
        return analytics_by_date
    except Exception as e:
        print(f"  Error extracting analytics for {model_id}: {e}")
        return None

def extract_parameters(model_name, model_id):
    """Extract parameter count from model name or id"""
    
    # First, check manual mapping (most reliable)
    if model_id in PARAMETER_MAP:
        return PARAMETER_MAP[model_id]
    
    import re
    
    text = (model_name + ' ' + model_id).lower()
    
    # Pattern: number + b (e.g., 120b, 70b, 7b, 1.2b)
    matches = re.findall(r'(\d+(?:\.\d+)?)\s*b', text)
    if matches:
        # Return the largest number found (likely the main parameter count)
        params = sorted(matches, key=lambda x: float(x), reverse=True)
        return f"{params[0]}B"
    
    # Additional patterns: 3.1b, 3.2b, 3.3b, 4.5b, 2.6b, 2.5b
    # Try patterns like "a12b", "a3b", "a4b" (MoE models)
    moe_matches = re.findall(r'a(\d+(?:\.\d+)?)\s*b', text)
    if moe_matches:
        params = sorted(moe_matches, key=lambda x: float(x), reverse=True)
        return f"A{params[0]}B"
    
    return None

def calculate_score(model_info, all_models):
    """Calculate a score from 0-5 based on usage, freshness, and benchmarks"""
    # For now, base score primarily on usage volume (normalized to 0-5)
    usage = model_info.get('usage_raw', 0)
    if not usage:
        return None
    
    # Get all usage values for normalization
    all_usages = [m.get('usage_raw', 0) for m in all_models if m.get('usage_raw')]
    if not all_usages:
        return None
    
    max_usage = max(all_usages)
    min_usage = min(all_usages)
    
    if max_usage == min_usage:
        return 2.5  # Default middle score
    
    # Normalize to 0-5 range (higher usage = higher score)
    normalized = (usage - min_usage) / (max_usage - min_usage)
    score = round(normalized * 5, 1)
    
    # Bonus for having tools/vision/reasoning
    if model_info.get('has_tools'):
        score += 0.2
    if model_info.get('has_vision'):
        score += 0.1
    if model_info.get('has_reasoning'):
        score += 0.1
    
    return min(round(score, 1), 5.0)  # Cap at 5.0

def main():
    print("Fetching models from OpenRouter API...")
    all_models = fetch_models()
    
    print(f"Total models fetched: {len(all_models)}")
    
    # Filter ONLY models with ':free' suffix
    free_models = [m for m in all_models if m.get('id', '').endswith(':free')]
    print(f"Models with ':free' suffix: {len(free_models)}")
    
    # Double-check they are actually free
    verified_free = [m for m in free_models if is_free_model(m)]
    print(f"Verified free models: {len(verified_free)}")
    
    # Get last_updated time (for analytics calculation)
    last_updated = datetime.now()
    
    # Extract info (pass last_updated for requests_per_day calculation)
    models_info = [extract_model_info(m, last_updated) for m in verified_free]
    
    # Calculate scores based on all models
    for model in models_info:
        score = calculate_score(model, models_info)
        if score is not None:
            model['score'] = score
    
    # Sort by usage volume (descending), then by context length
    models_info.sort(key=lambda x: (x['usage_raw'] or 0, x['context_length']), reverse=True)
    
    # Get unique providers
    providers = sorted(set(m['provider'] for m in models_info))
    
    # Prepare output data
    output = {
        'last_updated': last_updated.strftime('%Y-%m-%d %H:%M:%S UTC'),
        'total_models': len(models_info),
        'total_providers': len(providers),
        'providers': providers,
        'models': models_info
    }
    
    # Write to file
    with open('data/models.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Data written to data/models.json")
    print(f"Models: {len(models_info)}, Providers: {len(providers)}")
    
    # Show usage volumes
    print("\nModels with usage data:")
    for m in models_info:
        if m['usage_volume']:
            print(f"  - {m['name']}: {m['usage_volume']} tokens")

if __name__ == '__main__':
    main()
