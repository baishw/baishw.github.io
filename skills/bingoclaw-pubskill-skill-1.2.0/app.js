// 技能展示页面 JavaScript

const API_BASE_URL = 'https://skill.cxus.cn';

// 获取URL参数
function getUrlParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// 设置URL参数
function setUrlParam(name, value) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set(name, value);
    window.history.pushState({}, '', `${window.location.pathname}?${urlParams.toString()}`);
}

// 显示加载状态
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('error').classList.add('hidden');
    document.getElementById('skill-content').classList.add('hidden');
}

// 显示错误信息
function showError(message) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('skill-content').classList.add('hidden');
    document.getElementById('error').classList.remove('hidden');
    document.getElementById('error-message').textContent = message;
}

// 显示技能内容
function showSkillContent() {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    document.getElementById('skill-content').classList.remove('hidden');
}

// 根据技能类型获取图标
function getSkillIcon(type) {
    const icons = {
        'function': '🔧',
        'api': '🌐',
        'database': '🗄️',
        'workflow': '⚙️',
        'default': '✨'
    };
    return icons[type] || icons['default'];
}

// 根据风险等级获取样式类
function getRiskClass(risk) {
    const classes = {
        'low': 'badge-low',
        'medium': 'badge-medium',
        'high': 'badge-high'
    };
    return classes[risk] || classes['low'];
}

// 根据风险等级获取颜色
function getRiskColor(risk) {
    const colors = {
        'low': '#10b981',
        'medium': '#f59e0b',
        'high': '#ef4444'
    };
    return colors[risk] || colors['low'];
}

// 渲染技能信息
function renderSkill(skill) {
    // 基本信息
    document.getElementById('skill-icon').textContent = getSkillIcon(skill.type);
    document.getElementById('skill-name').textContent = skill.name || '未知技能';
    document.getElementById('skill-type').textContent = skill.type || 'function';
    document.getElementById('skill-version').textContent = 'v' + (skill.version || '1.0.0');
    
    // 风险等级
    const riskBadge = document.getElementById('skill-risk');
    riskBadge.textContent = skill.risk_level || 'low';
    riskBadge.style.backgroundColor = getRiskColor(skill.risk_level);
    
    // 描述
    document.getElementById('skill-description').textContent = skill.description || '暂无描述';
    
    // 提供者
    document.getElementById('skill-provider').textContent = skill.username || '未知提供者';
    
    // 技能ID
    document.getElementById('skill-id').textContent = skill.id || '-';
    
    // 时间信息
    document.getElementById('skill-created').textContent = skill.created_at ? formatDate(skill.created_at) : '-';
    document.getElementById('skill-updated').textContent = skill.updated_at ? formatDate(skill.updated_at) : '-';
    
    // 状态
    const statusElement = document.getElementById('skill-status');
    statusElement.textContent = skill.status === 'normal' ? '正常' : '禁用';
    statusElement.style.color = skill.status === 'normal' ? '#10b981' : '#ef4444';
    
    // 参数渲染
    renderParams(skill.params);
    
    // 返回结果渲染
    renderReturns(skill.returns);
    
    // 安装命令
    document.getElementById('install-command').textContent = `pip install ${skill.name || 'skill-package'}`;
    
    // 使用示例
    generateUsageExample(skill);
}

// 渲染参数列表
function renderParams(params) {
    const container = document.getElementById('skill-params');
    container.innerHTML = `
        <div class="param-card">
            <div class="param-name">参数名称</div>
            <div class="param-type">类型</div>
            <div class="param-desc">描述</div>
            <div class="param-required">必填</div>
        </div>
    `;
    
    if (!params || !params.properties) {
        container.innerHTML += `
            <div class="param-card">
                <div class="param-name">-</div>
                <div class="param-type">-</div>
                <div class="param-desc">暂无参数</div>
                <div class="param-required">-</div>
            </div>
        `;
        return;
    }
    
    const requiredFields = params.required || [];
    
    Object.keys(params.properties).forEach(key => {
        const prop = params.properties[key];
        const isRequired = requiredFields.includes(key);
        container.innerHTML += `
            <div class="param-card">
                <div class="param-name">${key}</div>
                <div class="param-type">${prop.type || 'string'}</div>
                <div class="param-desc">${prop.description || '-'}</div>
                <div class="param-required">${isRequired ? '是' : ''}</div>
            </div>
        `;
    });
}

// 渲染返回结果
function renderReturns(returns) {
    const container = document.getElementById('skill-returns');
    container.innerHTML = `
        <div class="param-card">
            <div class="param-name">返回字段</div>
            <div class="param-type">类型</div>
            <div class="param-desc">描述</div>
            <div class="param-required"></div>
        </div>
    `;
    
    if (!returns || !returns.properties) {
        container.innerHTML += `
            <div class="param-card">
                <div class="param-name">-</div>
                <div class="param-type">-</div>
                <div class="param-desc">暂无返回信息</div>
                <div class="param-required"></div>
            </div>
        `;
        return;
    }
    
    Object.keys(returns.properties).forEach(key => {
        const prop = returns.properties[key];
        container.innerHTML += `
            <div class="param-card">
                <div class="param-name">${key}</div>
                <div class="param-type">${prop.type || 'string'}</div>
                <div class="param-desc">${prop.description || '-'}</div>
                <div class="param-required"></div>
            </div>
        `;
    });
}

// 生成使用示例
function generateUsageExample(skill) {
    const example = document.getElementById('usage-example');
    const params = skill.params?.properties || {};
    const paramKeys = Object.keys(params).slice(0, 2);
    
    let code = `# 使用 ${skill.name || 'skill'} 技能\n`;
    code += `from skills import ${skill.name || 'skill_module'}\n\n`;
    
    if (paramKeys.length > 0) {
        code += `# 调用技能\n`;
        const paramStr = paramKeys.map(k => `${k}="${params[k]?.description || 'value'}"`).join(', ');
        code += `result = ${skill.name || 'execute_skill'}(${paramStr})\n`;
    } else {
        code += `# 调用技能\n`;
        code += `result = ${skill.name || 'execute_skill'}()\n`;
    }
    
    code += `\n# 处理结果\n`;
    code += `print(result)\n`;
    
    example.textContent = code;
}

// 格式化日期
function formatDate(timestamp) {
    if (!timestamp) return '-';
    const date = new Date(parseInt(timestamp) * 1000);
    return date.toLocaleDateString('zh-CN');
}

// 获取技能详情
async function fetchSkillDetail(skillId) {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/skill/detail?id=${skillId}`);
        const data = await response.json();
        
        if (response.ok && data.code === 1) {
            renderSkill(data.data);
            showSkillContent();
            setUrlParam('id', skillId);
        } else {
            showError(data.msg || '获取技能信息失败');
        }
    } catch (error) {
        showError('网络请求失败，请检查网络连接');
    }
}

// 搜索技能
async function searchSkills(keyword) {
    if (!keyword.trim()) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/skill/search?keyword=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        
        if (response.ok && data.code === 1) {
            renderSearchResults(data.data);
        } else {
            document.getElementById('search-results').innerHTML = '<p style="text-align:center;color:#999;">搜索失败</p>';
        }
    } catch (error) {
        document.getElementById('search-results').innerHTML = '<p style="text-align:center;color:#999;">网络请求失败</p>';
    }
}

// 渲染搜索结果
function renderSearchResults(skills) {
    const container = document.getElementById('search-results');
    
    if (!skills || skills.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:#999;">未找到匹配的技能</p>';
        return;
    }
    
    container.innerHTML = skills.map(skill => `
        <div class="skill-card" onclick="fetchSkillDetail(${skill.id})">
            <div class="skill-card-icon">${getSkillIcon(skill.type)}</div>
            <div class="skill-card-info">
                <div class="skill-card-title">${skill.name}</div>
                <div class="skill-card-desc">${skill.description || '暂无描述'}</div>
                <div class="skill-card-meta">
                    <span class="badge badge-type" style="background:#667eea;">${skill.type}</span>
                    <span class="badge badge-version" style="background:#10b981;">v${skill.version}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// 初始化页面
function init() {
    // 获取URL中的技能ID
    const skillId = getUrlParam('id');
    
    if (skillId) {
        // 如果有技能ID，直接加载技能详情
        fetchSkillDetail(skillId);
    } else {
        // 否则显示搜索界面
        showLoading();
        // 默认隐藏加载，显示搜索
        setTimeout(() => {
            document.getElementById('loading').classList.add('hidden');
            document.getElementById('search').scrollIntoView({ behavior: 'smooth' });
        }, 500);
    }
    
    // 搜索按钮事件
    document.getElementById('search-btn').addEventListener('click', () => {
        const keyword = document.getElementById('search-input').value;
        searchSkills(keyword);
    });
    
    // 回车键搜索
    document.getElementById('search-input').addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            searchSkills(e.target.value);
        }
    });
    
    // 重试按钮事件
    document.getElementById('retry-btn').addEventListener('click', () => {
        const skillId = getUrlParam('id');
        if (skillId) {
            fetchSkillDetail(skillId);
        }
    });
    
    // 导航链接平滑滚动
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
