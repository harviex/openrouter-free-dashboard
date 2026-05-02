// OpenRouter Free Models Dashboard - Main JavaScript
// Version: 2026-04-28-v3 - Fixed formatContextLength reference

let allModels = [];
let filteredModels = [];
let currentView = 'grid';
let currentLang = 'en';
let savedData = null;  // Store data for re-rendering on language change
let searchTerm = '';  // Global search term for highlighting

// i18n translations
const translations = {
    en: {
        title: 'OpenRouter Free Models',
        subtitle: 'Daily updated dashboard for free AI models',
        sort_by: 'Sort by:',
        sort_parameters_high: 'Parameters (High to Low)',
        sort_parameters_low: 'Parameters (Low to High)',
        sort_score: 'Score (Highest First)',
        sort_context_high: 'Context Length (High to Low)',
        sort_context_low: 'Context Length (Low to High)',
        sort_name: 'Name (A-Z)',
        sort_newest: 'Newest First',
        provider: 'Provider:',
        all_providers: 'All Providers',
        capabilities: 'Capabilities:',
        tools: 'Tools',
        vision: 'Vision',
        reasoning: 'Reasoning',
        search_placeholder: 'Search models...',
        grid_view: 'Grid',
        list_view: 'List',
        refresh: 'Refresh',
        loading: 'Loading models...',
        footer_data: 'Data sourced from <a href="https://openrouter.ai" target="_blank">OpenRouter.ai</a> & <a href="https://huggingface.co" target="_blank">HuggingFace.co</a>',
        footer_updated: 'Last updated: ',
        footer_inspired: 'Inspired by <a href="https://www.canirun.ai" target="_blank">CanIRun.ai</a>',
        copied_toast: 'Copied to clipboard!',
        copied: 'Copied: ',
        click_to_copy: 'Click to copy model ID',
        free_model: 'FREE',
        expires: 'Expires: ',
        no_expiry: 'No expiry',
        rating: 'Rating: ',
        models: 'Models',
        providers: 'Providers',
        rating_info: 'Rating Info',
        rating_formula: 'Score Formula:',
        rating_40_p: '40% - Community Popularity (Likes + Downloads from HuggingFace)',
        rating_20_f: '20% - Freshness (Days since model creation)',
        rating_40_b: '40% - Benchmark Performance (Presence of eval-results tag)',
        rating_range: 'Score Range: 0.0 - 5.0',
        rating_updated: 'Updated daily via GitHub Actions',
        details: 'Details',
        compare: 'Compare',
        max_compare: 'Maximum 3 models can be compared'
    },
    zh: {
        title: 'OpenRouter 免费模型面板',
        subtitle: '每日更新的免费AI模型仪表板',
        sort_by: '排序方式：',
        sort_parameters_high: '参数量（从高到低）',
        sort_parameters_low: '参数量（从低到高）',
        sort_score: '评分（从高到低）',
        sort_context_high: '上下文长度（从高到低）',
        sort_context_low: '上下文长度（从低到高）',
        sort_name: '名称（A到Z）',
        sort_newest: '最新优先',
        provider: '提供商：',
        all_providers: '所有提供商',
        capabilities: '功能：',
        tools: '工具',
        vision: '视觉',
        reasoning: '推理',
        search_placeholder: '搜索模型...',
        grid_view: '网格',
        list_view: '列表',
        refresh: '刷新',
        loading: '正在加载模型...',
        footer_data: '数据来源：<a href="https://openrouter.ai" target="_blank">OpenRouter.ai</a> & <a href="https://huggingface.co" target="_blank">HuggingFace.co</a>',
        footer_updated: '最后更新：',
        footer_inspired: '灵感来自 <a href="https://www.canirun.ai" target="_blank">CanIRun.ai</a>',
        copied_toast: '已复制到剪贴板！',
        copied: '已复制：',
        click_to_copy: '点击复制模型ID',
        free_model: '免费',
        expires: '限免到期：',
        no_expiry: '无限期',
        rating: '评分：',
        models: '模型',
        providers: '提供商',
        rating_info: '评分说明',
        rating_formula: '评分公式：',
        rating_40_p: '40% - 社区热度（HuggingFace 点赞 + 下载量）',
        rating_20_f: '20% - 新鲜度（模型创建天数）',
        rating_40_b: '40% - 基准性能（是否存在 eval-results 标签）',
        rating_range: '评分范围：0.0 - 5.0',
        rating_updated: '每日通过 GitHub Actions 更新',
        details: '详情',
        compare: '对比',
        max_compare: '最多可对比3个模型'
    },
    ja: {
        title: 'OpenRouter 無料モデルダッシュボード',
        subtitle: '無料AIモデルの日次更新ダッシュボード',
        sort_by: '並び替え：',
        sort_parameters_high: 'パラメータ数（多い順）',
        sort_parameters_low: 'パラメータ数（少ない順）',
        sort_score: 'スコア（高い順）',
        sort_context_high: 'コンテキスト長（長い順）',
        sort_context_low: 'コンテキスト長（短い順）',
        sort_name: '名前（A-Z）',
        sort_newest: '新しい順',
        provider: 'プロバイダー：',
        all_providers: 'すべてのプロバイダー',
        capabilities: '機能：',
        tools: 'ツール',
        vision: 'ビジョン',
        reasoning: '推論',
        search_placeholder: 'モデルを検索...',
        grid_view: 'グリッド',
        list_view: 'リスト',
        refresh: '更新',
        loading: 'モデルを読み込み中...',
        footer_data: 'データソース：<a href="https://openrouter.ai" target="_blank">OpenRouter.ai</a> & <a href="https://huggingface.co" target="_blank">HuggingFace.co</a>',
        footer_updated: '最終更新：',
        footer_inspired: '<a href="https://www.canirun.ai" target="_blank">CanIRun.ai</a>にインスパイアされました',
        copied_toast: 'クリップボードにコピーしました！',
        copied: 'コピーしました：',
        click_to_copy: 'クリックしてモデルIDをコピー',
        free_model: '無料',
        expires: '期限：',
        no_expiry: '無期限',
        rating: '評価：',
        models: 'モデル',
        providers: 'プロバイダー',
        rating_info: '評価について',
        rating_formula: 'スコア計算式：',
        rating_40_p: '40% - コミュニティ人気（いいね + ダウンロード数）',
        rating_20_f: '20% - 新しさ（モデル作成からの日数）',
        rating_40_b: '40% - ベンチマーク性能（eval-resultsタグの有無）',
        rating_range: 'スコア範囲：0.0 - 5.0',
        rating_updated: '毎日GitHub Actionsで更新',
        details: '詳細',
        compare: '比較',
        max_compare: '最大3つのモデルを比較できます'
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Set theme from localStorage or default to light
    initTheme();
    
    // Set language
    const savedLang = localStorage.getItem('language') || 'en';
    document.getElementById('languageSelect').value = savedLang;
    changeLanguage();
    
    loadModels();
    getGitHubStars();
});

// Theme functions
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    let newTheme;
    
    if (currentTheme === 'light') {
        newTheme = 'dark';
    } else {
        newTheme = 'light';
    }
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const btn = document.getElementById('themeToggle');
    if (theme === 'light') {
        btn.textContent = '☀️';
        btn.title = 'Switch to dark mode';
    } else {
        btn.textContent = '🌙';
        btn.title = 'Switch to light mode';
    }
}

// Language functions
function changeLanguage() {
    currentLang = document.getElementById('languageSelect').value;
    localStorage.setItem('language', currentLang);
    applyTranslations();
    
    // Re-render stats with new language
    if (savedData) {
        updateStats(savedData);
    }
    
    // Re-render models with new language
    renderModels();
}

function applyTranslations() {
    const t = translations[currentLang];
    
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            if (el.tagName === 'INPUT' && el.hasAttribute('data-i18n-placeholder')) {
                el.placeholder = t[key];
            } else if (el.innerHTML.includes('<') === false) {
                el.textContent = t[key];
            }
        }
    });
    
    // Update select options
    document.querySelectorAll('[data-i18n-option]').forEach(option => {
        const key = option.getAttribute('data-i18n-option');
        if (t[key]) {
            option.textContent = t[key];
        }
    });
}

// Load models from JSON file
async function loadModels() {
    try {
        const response = await fetch('data/models.json?t=' + new Date().getTime());
        if (!response.ok) throw new Error('Failed to load models');
        
        const data = await response.json();
        allModels = data.models || [];
        savedData = data;  // Save for language re-render
        
        updateStats(data);
        populateProviders();
        applyFilters();
    } catch (error) {
        console.error('Error loading models:', error);
        document.getElementById('modelsContainer').innerHTML = 
            '<div class="loading">' + translations[currentLang].loading + '</div>';
    }
}

// Update stats in navbar
function updateStats(data) {
    const totalModels = data.total_models || allModels.length;
    const totalProviders = data.total_providers || new Set(allModels.map(m => m.provider)).size;
    const t = translations[currentLang];
    
    document.getElementById('stats').innerHTML = `
        <span class="stat-item">📊 ${totalModels} ${t.free_model} ${t.models}</span>
        <span class="stat-item">🏢 ${totalProviders} ${t.providers}</span>
        <span class="stat-item">📅 ${data.last_updated || 'Unknown'}</span>
    `;
}

// Populate provider filter dropdown
function populateProviders() {
    const providers = [...new Set(allModels.map(m => m.provider))].sort();
    const select = document.getElementById('providerFilter');
    
    // Clear existing options except first
    while (select.options.length > 1) {
        select.remove(1);
    }
    
    providers.forEach(provider => {
        const option = document.createElement('option');
        option.value = provider;
        option.textContent = provider;
        select.appendChild(option);
    });
}

// Apply all filters and render
function applyFilters() {
    const providerFilter = document.getElementById('providerFilter').value;
    const sortBy = document.getElementById('sortBy').value;
    searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filterTools = document.getElementById('filterTools').checked;
    const filterVision = document.getElementById('filterVision').checked;
    const filterReasoning = document.getElementById('filterReasoning').checked;
    
    // Start with all models
    filteredModels = [...allModels];
    
    // Filter by provider
    if (providerFilter !== 'all') {
        filteredModels = filteredModels.filter(m => m.provider === providerFilter);
    }
    
    // Filter by capabilities
    if (filterTools) {
        filteredModels = filteredModels.filter(m => m.has_tools);
    }
    if (filterVision) {
        filteredModels = filteredModels.filter(m => m.has_vision);
    }
    if (filterReasoning) {
        filteredModels = filteredModels.filter(m => m.has_reasoning);
    }
    
    // Filter by search term
    if (searchTerm) {
        filteredModels = filteredModels.filter(m => 
            m.name.toLowerCase().includes(searchTerm) ||
            m.id.toLowerCase().includes(searchTerm) ||
            m.provider.toLowerCase().includes(searchTerm)
        );
    }
    
    // Sort
    switch(sortBy) {
        case 'parameters_high':
            filteredModels.sort((a, b) => parseParameters(b.parameters) - parseParameters(a.parameters));
            break;
        case 'parameters_low':
            filteredModels.sort((a, b) => parseParameters(a.parameters) - parseParameters(b.parameters));
            break;
        case 'score':
            filteredModels.sort((a, b) => (b.score || 0) - (a.score || 0));
            break;
        case 'context_length':
            filteredModels.sort((a, b) => b.context_length - a.context_length);
            break;
        case 'context_length_asc':
            filteredModels.sort((a, b) => a.context_length - b.context_length);
            break;
        case 'name':
            filteredModels.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'created':
            filteredModels.sort((a, b) => b.created - a.created);
            break;
    }
    
    renderModels();
}

// Render model cards
function renderModels() {
    const container = document.getElementById('modelsContainer');
    container.className = `models-container ${currentView}-view`;
    
    if (allModels.length === 0) {
        container.innerHTML = '<div class="loading">⚠️ Failed to load models. Please refresh the page.</div>';
        return;
    }
    
    if (filteredModels.length === 0) {
        container.innerHTML = '<div class="loading">🔍 No models match your filters. Try adjusting the filters.</div>';
        return;
    }
    
    container.innerHTML = filteredModels.map(model => createModelCard(model)).join('');
}

// Create HTML for a model card
function createModelCard(model) {
    const t = translations[currentLang];
    const capabilities = [];
    if (model.has_tools) capabilities.push('<span class="capability-tag">🔧 ' + t.tools + '</span>');
    if (model.has_vision) capabilities.push('<span class="capability-tag">👁️ ' + t.vision + '</span>');
    if (model.has_reasoning) capabilities.push('<span class="capability-tag">💭 ' + t.reasoning + '</span>');
    
    const contextLength = formatContextLength(model.context_length);
    const createdDate = formatDate(model.created);
    const expiryInfo = formatExpiry(model.expiration_date);
    const copyHint = t.click_to_copy + ' ' + model.id;
    
    // Highlight search terms
    const highlightedName = highlightText(model.name, searchTerm);
    const highlightedId = highlightText(model.id, searchTerm);
    const highlightedProvider = highlightText(model.provider, searchTerm);
    
    // Build footer content: FREE badge + optional expiry (inline)
    let footerContent = '<span class="free-badge">' + t.free_model + '</span>';
    if (expiryInfo) {
        footerContent += '<span class="expiration-inline">' + t.expires + expiryInfo + '</span>';
    }
    
    if (currentView === 'list') {
        return `
            <div class="model-card list-view" onclick="copyModelId('${model.id}')" title="${copyHint}">
                <input type="checkbox" class="compare-checkbox" onchange="event.stopPropagation(); toggleCompare('${model.id}')">
                <div class="card-header">
                    <span class="provider-badge">${highlightedProvider}</span>
                    <div class="model-name"><a href="${model.model_url || '#'}" target="_blank" onclick="event.stopPropagation()">${highlightedName}</a></div>
                    <div class="model-id">${highlightedId}</div>
                </div>
                <div class="card-body">
                    <div class="card-stats">
                        <span class="stat">📏 ${contextLength}</span>
                        <span class="stat">📊 ${model.parameters || 'N/A'}${model.paid_pricing ? ` | $${model.paid_pricing.prompt}/$${model.paid_pricing.completion}/1M` : ''}</span>
                        ${model.score !== null && model.score !== undefined ? `<span class="stat">⭐ ${model.score}/5.0 <span class="info-icon" onclick="event.stopPropagation(); openRatingModal()">ℹ️</span></span>` : ''}
                        <span class="stat">📅 ${createdDate}</span>
                    </div>
                    <div class="capabilities">${capabilities.join('')}</div>
                </div>
                <div class="card-footer">
                    ${footerContent}
                    <button class="expand-btn" onclick="event.stopPropagation(); toggleDetails('${model.id.replace(/[^a-zA-Z0-9]/g, '_')}')">${t.details || 'Details'} ▼</button>
                </div>
                <div class="model-details" id="details_${model.id.replace(/[^a-zA-Z0-9]/g, '_')}">
                    <div class="details-content">
                        <p><strong>${t.description || 'Description'}:</strong> ${model.description || 'N/A'}</p>
                        <p><strong>${t.supported_params || 'Supported Parameters'}:</strong> ${model.supported_parameters ? model.supported_parameters.join(', ') : 'None'}</p>
                        <p><strong>${t.created || 'Created'}:</strong> ${createdDate}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    return `
        <div class="model-card" onclick="copyModelId('${model.id}')" title="${copyHint}">
            <input type="checkbox" class="compare-checkbox" onchange="event.stopPropagation(); toggleCompare('${model.id}')">
            <div class="card-header">
                <span class="provider-badge">${highlightedProvider}</span>
                <div class="model-name"><a href="${model.model_url || '#'}" target="_blank" onclick="event.stopPropagation()">${highlightedName}</a></div>
                <div class="model-id">${highlightedId}</div>
            </div>
            <div class="card-body">
                <div class="card-stats">
                    <span class="stat">📏 ${contextLength}</span>
                    <span class="stat">📊 ${model.parameters || 'N/A'}${model.paid_pricing ? ` | $${model.paid_pricing.prompt}/$${model.paid_pricing.completion}/1M` : ''}</span>
                </div>
                <div class="capabilities">${capabilities.join('')}</div>
                <div class="card-stats">
                    ${model.score !== null && model.score !== undefined ? `<span class="stat">⭐ ${model.score}/5.0 <span class="info-icon" onclick="event.stopPropagation(); openRatingModal()">ℹ️</span></span>` : ''}
                    <span class="stat">📅 ${createdDate}</span>
                </div>
            </div>
            <div class="card-footer">
                ${footerContent}
            </div>
        </div>
    `;
}

// Copy model ID to clipboard (with fallback)
function copyModelId(modelId) {
    // Try modern Clipboard API first
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(modelId).then(() => {
            showToast(translations[currentLang].copied + modelId);
        }).catch(err => {
            console.error('Clipboard API failed:', err);
            fallbackCopy(modelId);
        });
    } else {
        fallbackCopy(modelId);
    }
}

// Fallback copy method
function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showToast(translations[currentLang].copied + text);
        } else {
            showToast(translations[currentLang].copied + text + ' (manual copy needed)');
        }
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showToast('Failed to copy. Please copy manually: ' + text);
    }
    
    document.body.removeChild(textarea);
}

// Show toast notification
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Set view mode (grid/list)
function setView(view) {
    currentView = view;
    document.getElementById('gridView').classList.toggle('active', view === 'grid');
    document.getElementById('listView').classList.toggle('active', view === 'list');
    renderModels();
}

// Refresh data
function refreshData() {
    showToast(translations[currentLang].loading);
    loadModels();
}

// Utility: Parse parameters string to number for sorting
function parseParameters(paramStr) {
    if (!paramStr || paramStr === 'Unknown') return 0;
    
    // Extract number and unit
    const match = paramStr.match(/(\d+\.?\d*)\s*([BT])?/i);
    if (!match) return 0;
    
    const value = parseFloat(match[1]);
    const unit = (match[2] || 'B').toUpperCase();
    
    // Convert to B (Billions)
    if (unit === 'T') {
        return value * 1000; // 1T = 1000B
    }
    return value; // Already in B
}

// Utility: Format context length
function formatContextLength(length) {
    if (length >= 1000000) {
        return (length / 1000000).toFixed(1) + 'M ctx';
    } else if (length >= 1000) {
        return (length / 1000).toFixed(0) + 'K ctx';
    }
    return length + ' ctx';
}

// Utility: Format date
function formatDate(timestamp) {
    if (!timestamp) return 'Unknown';
    const date = new Date(timestamp * 1000);
    return date.toLocaleDateString(currentLang === 'zh' ? 'zh-CN' : currentLang === 'ja' ? 'ja-JP' : 'en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// Utility: Format expiry date
function formatExpiry(expiryDate) {
    if (!expiryDate) return null;
    
    const date = new Date(expiryDate);
    const now = new Date();
    const daysLeft = Math.ceil((date - now) / (1000 * 60 * 60 * 24));
    
    if (daysLeft < 0) {
        return 'Expired';
    } else if (daysLeft <= 7) {
        return expiryDate + ` (${daysLeft}d left)`;
    }
    
    return expiryDate;
}

// GitHub Star Count
async function getGitHubStars() {
    try {
        const response = await fetch('https://api.github.com/repos/harviex/openrouter-free-dashboard');
        if (response.ok) {
            const data = await response.json();
            const stars = data.stargazers_count || 0;
            const starCountEl = document.getElementById('starCount');
            if (starCountEl) {
                starCountEl.textContent = stars;
            }
        }
    } catch (error) {
        console.error('Failed to fetch GitHub stars:', error);
    }
}

// Rating Modal functions
function openRatingModal() {
    const modal = document.getElementById('ratingModal');
    const title = document.getElementById('ratingModalTitle');
    const body = document.getElementById('ratingModalBody');
    const t = translations[currentLang];
    
    title.textContent = t.rating_info;
    body.innerHTML = `
        <p><strong>${t.rating_formula}</strong></p>
        <ul>
            <li><strong>40%</strong> - ${t.rating_40_p}</li>
            <li><strong>20%</strong> - ${t.rating_20_f}</li>
            <li><strong>40%</strong> - ${t.rating_40_b}</li>
        </ul>
        <p><strong>${t.rating_range}</strong></p>
        <p><em>${t.rating_updated}</em></p>
    `;
    
    modal.style.display = 'block';
}

function closeRatingModal() {
    document.getElementById('ratingModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('ratingModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Toggle model details
function toggleDetails(modelId) {
    const detailsId = 'details_' + modelId.replace(/[^a-zA-Z0-9]/g, '_');
    const detailsEl = document.getElementById(detailsId);
    const btn = event.target;
    
    if (detailsEl.classList.contains('expanded')) {
        detailsEl.classList.remove('expanded');
        btn.textContent = (translations[currentLang].details || 'Details') + ' ▼';
    } else {
        // Close other open details first
        document.querySelectorAll('.model-details.expanded').forEach(el => {
            el.classList.remove('expanded');
        });
        document.querySelectorAll('.expand-btn').forEach(btn => {
            btn.textContent = (translations[currentLang].details || 'Details') + ' ▼';
        });
        
        detailsEl.classList.add('expanded');
        btn.textContent = (translations[currentLang].details || 'Details') + ' ▲';
    }
}

// Search highlight function
function highlightText(text, searchTerm) {
    if (!text || !searchTerm) return text;
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

// Compare functionality
let compareList = [];

function toggleCompare(modelId) {
    const index = compareList.indexOf(modelId);
    if (index > -1) {
        compareList.splice(index, 1);
    } else {
        if (compareList.length >= 3) {
            alert('Maximum 3 models can be compared');
            // Uncheck the checkbox
            event.target.checked = false;
            return;
        }
        compareList.push(modelId);
    }
    updateCompareButton();
}

function updateCompareButton() {
    const t = translations[currentLang];
    let btn = document.getElementById('compareBtn');
    if (!btn) {
        // Create button if not exists
        btn = document.createElement('button');
        btn.id = 'compareBtn';
        btn.className = 'compare-btn';
        btn.onclick = showCompareModal;
        document.body.appendChild(btn);
    }
    if (compareList.length >= 2) {
        btn.classList.add('show');
        btn.textContent = `${t.compare || 'Compare'} ${compareList.length} ${(t.compare || 'Compare') === 'Compare' ? 'Models' : ''}`;
    } else {
        btn.classList.remove('show');
    }
}

function showCompareModal() {
    if (compareList.length < 2) return;
    
    const modal = document.getElementById('compareModal');
    const title = document.getElementById('compareTitle');
    const content = document.getElementById('compareContent');
    
    const models = compareList.map(id => allModels.find(m => m.id === id)).filter(Boolean);
    
    title.textContent = `Model Comparison (${models.length})`;
    
    let html = '<table class="compare-table"><tr><th>Attribute</th>';
    models.forEach(m => { html += `<th>${m.name}</th>`; });
    html += '</tr>';
    
    // ID
    html += '<tr><td><strong>ID</strong></td>';
    models.forEach(m => { html += `<td>${m.id}</td>`; });
    html += '</tr>';
    
    // Provider
    html += '<tr><td><strong>Provider</strong></td>';
    models.forEach(m => { html += `<td>${m.provider}</td>`; });
    html += '</tr>';
    
    // Parameters
    html += '<tr><td><strong>Parameters</strong></td>';
    models.forEach(m => { html += `<td>${m.parameters || 'N/A'}</td>`; });
    html += '</tr>';
    
    // Context Length
    html += '<tr><td><strong>Context Length</strong></td>';
    models.forEach(m => { html += `<td>${formatContextLength(m.context_length)}</td>`; });
    html += '</tr>';
    
    // Score
    html += '<tr><td><strong>Score</strong></td>';
    models.forEach(m => { html += `<td>${m.score ? m.score + '/5.0' : 'N/A'}</td>`; });
    html += '</tr>';
    
    // Tools
    html += '<tr><td><strong>Tools</strong></td>';
    models.forEach(m => { html += `<td>${m.has_tools ? '✅' : '❌'}</td>`; });
    html += '</tr>';
    
    // Vision
    html += '<tr><td><strong>Vision</strong></td>';
    models.forEach(m => { html += `<td>${m.has_vision ? '✅' : '❌'}</td>`; });
    html += '</tr>';
    
    // Reasoning
    html += '<tr><td><strong>Reasoning</strong></td>';
    models.forEach(m => { html += `<td>${m.has_reasoning ? '✅' : '❌'}</td>`; });
    html += '</tr>';
    
    html += '</table>';
    content.innerHTML = html;
    modal.style.display = 'block';
}

function closeCompareModal() {
    document.getElementById('compareModal').style.display = 'none';
}

// Close modals when clicking outside
window.onclick = function(event) {
    const ratingModal = document.getElementById('ratingModal');
    const compareModal = document.getElementById('compareModal');
    if (event.target == ratingModal) {
        ratingModal.style.display = 'none';
    }
    if (event.target == compareModal) {
        compareModal.style.display = 'none';
    }
};
