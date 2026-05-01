#!/usr/bin/env python3
"""
Fetch free models from OpenRouter API and generate JSON data file
Only includes models with ':free' suffix. Adds Artificial Analysis scores.
"""
import json
import urllib.request
from datetime import datetime

# Artificial Analysis API 配置
AA_API_KEY = "aa_SqQxrWaNbnLuwAHUNogkGrSNZOngsxzy"
AA_API_URL = "https://artificialanalysis.ai/api/v2/data/llms/models"
aa_models_cache = None

# OpenRouter 模型名 → AA 模型名映射表（手动匹配）
OPENROUTER_TO_AA = {
    # 已验证匹配
    "Tencent: Hy3 preview (free)": "Hy3-preview (Non-reasoning)",
    "NVIDIA: Nemotron 3 Super (free)": "Llama 3.1 Nemotron Instruct 70B",
    "Google: Gemma 4 31B (free)": "Gemma 4 31B (Non-reasoning)",
    "MiniMax: MiniMax M2.5 (free)": "MiniMax-M2.5",
    "inclusionAI: Ling-2.6-1T (free)": "Ling 2.6 Flash",
    "Baidu: Qianfan-OCR-Fast (free)": "ERNIE 5.0 Thinking Preview",
    "NVIDIA: Nemotron 3 Nano Omni (free)": "NVIDIA Nemotron Nano 12B v2 VL (Reasoning)",
    "Qwen: Qwen3 Next 80B A3B Instruct (free)": "Qwen3 Next 80B A3B Instruct",
    "OpenAI: gpt-oss-20b (free)": "gpt-oss-20B (low)",
    "OpenAI: gpt-oss-120b (free)": "gpt-oss-120B (low)",
    
    # 新增匹配（从AA数据库找到的）
    "Meta: Llama 3.3 70B Instruct (free)": "Llama 3.3 Instruct 70B",
    "Meta: Llama 3.2 3B Instruct (free)": "Llama 3.2 Instruct 3B",
    "NVIDIA: Nemotron 3 Nano 30B A3B (free)": "NVIDIA Nemotron 3 Nano 30B A3B (Reasoning)",
    "NVIDIA: Nemotron Nano 12B 2 VL (free)": "NVIDIA Nemotron Nano 12B v2 VL (Reasoning)",
    "NVIDIA: Nemotron Nano 9B V2 (free)": "NVIDIA Nemotron Nano 9B V2 (Reasoning)",
    "Qwen: Qwen3 Coder 480B A35B (free)": "Qwen3 Coder Next",
    "LiquidAI: LFM2.5-1.2B-Thinking (free)": "LFM2.5-1.2B-Thinking",
    "LiquidAI: LFM2.5-1.2B-Instruct (free)": "LFM2.5-1.2B-Instruct",
    "Z.ai: GLM 4.5 Air (free)": "GLM-5 (Non-reasoning)",  # 近似匹配
    "Google: Gemma 4 26B A4B (free)": "Gemma 4 26B A4B (Reasoning)",
    "Google: Gemma 3n 2B (free)": None,  # AA中可能没有
    "Google: Gemma 3n 4B (free)": None,
    "Google: Gemma 3 4B (free)": None,
    "Google: Gemma 3 12B (free)": None,
    "Google: Gemma 3 27B (free)": None,
    
    # 明确无对应
    "Poolside: Laguna XS.2 (free)": None,
    "Poolside: Laguna M.1 (free)": None,
    "Venice: Uncensored (free)": None,
}

def fetch_aa_models():
    """获取 Artificial Analysis 所有模型数据"""
    headers = {"x-api-key": AA_API_KEY}
    try:
        req = urllib.request.Request(AA_API_URL, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get('status') == 200:
                return data.get('data', [])
    except Exception as e:
        print(f"获取 AA 模型数据失败: {e}")
    return []

def get_aa_models():
    """获取缓存的 AA 模型数据"""
    global aa_models_cache
    if aa_models_cache is None:
        aa_models_cache = fetch_aa_models()
    return aa_models_cache

def find_aa_model(or_model_name, aa_models):
    """通过映射表或模糊匹配找到对应的 AA 模型"""
    # 1. 先查映射表
    aa_target_name = OPENROUTER_TO_AA.get(or_model_name)
    if aa_target_name is None:
        return None  # 映射表中明确标记为无对应
    
    if aa_target_name:
        for aa_model in aa_models:
            if aa_model['name'] == aa_target_name:
                return aa_model
    
    # 2. 模糊匹配：去掉 provider 前缀和 "(free)" 后缀
    clean_name = or_model_name.split(': ', 1)[-1].replace(' (free)', '').strip()
    for aa_model in aa_models:
        aa_clean = aa_model['name'].split(' (')[0].strip()  # 去掉 "(Reasoning)" 等后缀
        if clean_name.lower() in aa_clean.lower() or aa_clean.lower() in clean_name.lower():
            return aa_model
    
    return None

def fetch_models():
    """从 OpenRouter API 获取所有模型"""
    url = "https://openrouter.ai/api/v1/models"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data.get('data', [])
    except Exception as e:
        print(f"获取 OpenRouter 模型失败: {e}")
        return []

def is_free_model(model):
    """检查模型是否为免费模型（ID 以 ':free' 结尾）"""
    return model['id'].endswith(':free')

def extract_model_info(model):
    """提取模型信息 + 获取 AA 评分"""
    model_id = model['id']
    model_name = model.get('name', model_id)
    
    # 获取 AA 评分
    aa_scores = None
    aa_model_obj = None
    aa_models = get_aa_models()
    if aa_models:
        aa_model_obj = find_aa_model(model_name, aa_models)
        if aa_model_obj:
            evaluations = aa_model_obj.get('evaluations', {})
            aa_scores = {
                'intelligence': evaluations.get('artificial_analysis_intelligence_index'),
                'coding': evaluations.get('artificial_analysis_coding_index'),
                'math': evaluations.get('artificial_analysis_math_index'),
                'speed': aa_model_obj.get('median_output_tokens_per_second'),
                'aa_name': aa_model_obj['name']  # 记录匹配的 AA 模型名
            }
    
    # 构建结果
    return {
        "id": model_id,
        "name": model_name,
        "description": model.get('description', ''),
        "context_length": model.get('context_length', 4096),
        "pricing": model.get('pricing', {}),
        "created": model.get('created', 0),
        "intelligence_score": aa_scores.get('intelligence') if aa_scores else None,
        "coding_score": aa_scores.get('coding') if aa_scores else None,
        "score_display": f"AI指数: {aa_scores['intelligence']:.1f}" if (aa_scores and aa_scores.get('intelligence')) else None,
        "aa_model_name": aa_scores.get('aa_name') if aa_scores else None,
        "aa_evaluations": aa_model_obj.get('evaluations', {}) if aa_model_obj else {},  # 保存完整评估数据
        "top_provider": model.get('top_provider', {}),
        "per_request_limits": model.get('per_request_limits', {}),
        "architecture": model.get('architecture', {}),
    }

def main():
    print("正在获取 OpenRouter 模型...")
    all_models = fetch_models()
    print(f"获取到 {len(all_models)} 个模型")
    
    free_models = [m for m in all_models if is_free_model(m)]
    print(f"发现 {len(free_models)} 个免费模型")
    
    models_info = [extract_model_info(m) for m in free_models]
    
    output = {
        "generated_at": datetime.now().isoformat(),
        "count": len(models_info),
        "models": models_info
    }
    
    with open('models.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    # 统计结果
    scored = [m for m in models_info if m['intelligence_score']]
    print(f"\n已生成 models.json ({len(models_info)} 个模型)")
    print(f"✅ {len(scored)} 个模型成功匹配 AA 评分:")
    for m in scored:
        print(f"  ✓ {m['name']} → {m['aa_model_name']}: {m['score_display']}")
    
    unscored = [m for m in models_info if not m['intelligence_score']]
    if unscored:
        print(f"\n⚠️ {len(unscored)} 个模型未匹配到 AA 数据:")
        for m in unscored:
            print(f"  ✗ {m['name']}")

if __name__ == "__main__":
    main()