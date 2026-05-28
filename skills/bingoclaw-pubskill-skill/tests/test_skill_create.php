<?php
/**
 * 测试接口: /api/skill/create
 * 测试网站: https://skill.cxus.cn
 * 测试账号: skillpuber / 123456
 */

define('BASE_URL', 'https://skill.cxus.cn');
define('TEST_ACCOUNT', 'skillpuber');
define('TEST_PASSWORD', '123456');
define('DEBUG_MODE', true);

/**
 * 发送 HTTP 请求
 */
function httpRequest($url, $method = 'GET', $data = null, $headers = [])
{
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);

    $requestHeaders = ['Content-Type: application/x-www-form-urlencoded'];
    foreach ($headers as $key => $value) {
        $requestHeaders[] = "$key: $value";
    }
    curl_setopt($ch, CURLOPT_HTTPHEADER, $requestHeaders);

    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        if ($data !== null) {
            if (is_array($data) && isset($data['json'])) {
                curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
                curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data['json']));
            } else {
                curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
            }
        }
    }

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);

    curl_close($ch);

    return [
        'code' => $httpCode,
        'body' => $response,
        'error' => $error,
        'decoded' => json_decode($response, true)
    ];
}

/**
 * 打印测试结果
 */
function printResult($testName, $response, $expectedCode = null)
{
    $passed = false;
    if ($expectedCode !== null) {
        $passed = ($response['code'] === 200 && $response['decoded']['code'] === $expectedCode);
    } else {
        $passed = ($response['code'] === 200);
    }
    
    $status = $passed ? '✓ PASS' : '✗ FAIL';

    echo "\n" . str_repeat('=', 70) . "\n";
    echo "$status 测试: $testName\n";
    echo str_repeat('-', 70) . "\n";

    if (DEBUG_MODE || !$passed) {
        echo "HTTP 状态码: {$response['code']}\n";
        if ($response['decoded']) {
            echo "响应内容:\n";
            echo json_encode($response['decoded'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n";
        } else {
            echo "响应内容: {$response['body']}\n";
        }
    }

    if ($error = $response['error']) {
        echo "cURL 错误: $error\n";
    }

    return $passed;
}

// ==================== 主程序 ====================

echo "\n";
echo str_repeat('*', 70) . "\n";
echo "* 技能创建接口测试 /api/skill/create\n";
echo "* 测试网站: " . BASE_URL . "\n";
echo "* 测试账号: " . TEST_ACCOUNT . "\n";
echo "* 时间: " . date('Y-m-d H:i:s') . "\n";
echo str_repeat('*', 70) . "\n";

$testResults = [];
$token = '';
$createdSkillId = null;

// 步骤1: 登录获取Token
echo "\n\n" . str_repeat('#', 70) . "\n";
echo "步骤 1: 用户登录获取Token\n";
echo str_repeat('#', 70) . "\n";

$response = httpRequest(BASE_URL . '/api/user/login', 'POST', [
    'account' => TEST_ACCOUNT,
    'password' => TEST_PASSWORD
]);

$passed = printResult('登录获取Token', $response, 1);
$testResults['login'] = $passed;

if ($passed && isset($response['decoded']['data']['userinfo']['token'])) {
    $token = $response['decoded']['data']['userinfo']['token'];
    echo "\n  ✓ 成功获取Token: " . substr($token, 0, 20) . "...\n";
} else {
    echo "\n  ✗ 登录失败，无法继续测试\n";
    exit(1);
}

// 步骤2: 测试创建function类型技能
echo "\n\n" . str_repeat('#', 70) . "\n";
echo "步骤 2: 创建function类型技能\n";
echo str_repeat('#', 70) . "\n";

$functionSkillData = [
    'name' => 'test_function_skill_' . time(),
    'username' => TEST_ACCOUNT,
    'type' => 'function',
    'version' => '1.0.0',
    'description' => '测试技能描述 - 用于单元测试',
    'summary' => '测试技能摘要',
    'params' => '{"type":"object","properties":{"input":{"type":"string"}}}',
    'returns' => '{"type":"object","properties":{"result":{"type":"string"}}}',
    'dependencies' => '[]',
    'risk_level' => 'low',
    'rate_limit' => 100,
    'timeout' => 30,
    'method' => 'POST',
    'auth_type' => 'none',
    'icon' => ''
];

$response = httpRequest(BASE_URL . '/api/skill/create', 'POST', $functionSkillData, [
    'Token' => $token
]);

$passed = printResult('创建function技能', $response, 1);
$testResults['create_function'] = $passed;

if ($passed && isset($response['decoded']['data']['id'])) {
    $createdSkillId = $response['decoded']['data']['id'];
    echo "\n  ✓ 成功创建技能，ID: $createdSkillId\n";
}

// 步骤3: 测试创建api类型技能
echo "\n\n" . str_repeat('#', 70) . "\n";
echo "步骤 3: 创建api类型技能\n";
echo str_repeat('#', 70) . "\n";

$apiSkillData = [
    'name' => 'test_api_skill_' . time(),
    'username' => TEST_ACCOUNT,
    'type' => 'api',
    'version' => '1.0.0',
    'description' => 'API类型技能测试',
    'endpoint' => 'https://api.example.com/test',
    'method' => 'GET',
    'risk_level' => 'medium',
    'auth_type' => 'none'
];

$response = httpRequest(BASE_URL . '/api/skill/create', 'POST', $apiSkillData, [
    'Token' => $token
]);

$passed = printResult('创建api技能', $response, 1);
$testResults['create_api'] = $passed;

// 步骤4: 测试JSON格式创建技能
echo "\n\n" . str_repeat('#', 70) . "\n";
echo "步骤 4: JSON格式创建技能\n";
echo str_repeat('#', 70) . "\n";

$jsonSkillData = [
    'json' => [
        'name' => 'test_json_skill_' . time(),
        'username' => TEST_ACCOUNT,
        'type' => 'function',
        'version' => '1.0.0',
        'description' => 'JSON格式创建的技能',
        'risk_level' => 'low'
    ]
];

$response = httpRequest(BASE_URL . '/api/skill/create', 'POST', $jsonSkillData, [
    'Token' => $token
]);

$passed = printResult('JSON格式创建技能', $response, 1);
$testResults['create_json'] = $passed;

// 步骤5: 测试缺少必填字段
echo "\n\n" . str_repeat('#', 70) . "\n";
echo "步骤 5: 缺少必填字段（预期失败）\n";
echo str_repeat('#', 70) . "\n";

$incompleteData = [
    'version' => '1.0.0',
    'description' => '缺少必填字段的测试'
    // 缺少: name, username, type
];

$response = httpRequest(BASE_URL . '/api/skill/create', 'POST', $incompleteData, [
    'Token' => $token
]);

$passed = printResult('缺少必填字段', $response, 0); // 预期返回错误码0
$testResults['missing_fields'] = $passed;

// 步骤6: 测试无效的类型
echo "\n\n" . str_repeat('#', 70) . "\n";
echo "步骤 6: 无效的技能类型（预期失败）\n";
echo str_repeat('#', 70) . "\n";

$invalidTypeData = [
    'name' => 'test_invalid_type',
    'username' => TEST_ACCOUNT,
    'type' => 'invalid_type', // 无效类型
    'version' => '1.0.0'
];

$response = httpRequest(BASE_URL . '/api/skill/create', 'POST', $invalidTypeData, [
    'Token' => $token
]);

$passed = printResult('无效类型', $response, 0); // 预期返回错误码0
$testResults['invalid_type'] = $passed;

// 步骤7: 测试无效的风险等级
echo "\n\n" . str_repeat('#', 70) . "\n";
echo "步骤 7: 无效的风险等级（预期失败）\n";
echo str_repeat('#', 70) . "\n";

$invalidRiskData = [
    'name' => 'test_invalid_risk',
    'username' => TEST_ACCOUNT,
    'type' => 'function',
    'risk_level' => 'invalid_risk' // 无效风险等级
];

$response = httpRequest(BASE_URL . '/api/skill/create', 'POST', $invalidRiskData, [
    'Token' => $token
]);

$passed = printResult('无效风险等级', $response, 0); // 预期返回错误码0
$testResults['invalid_risk'] = $passed;

// 步骤8: 未登录状态创建技能（预期失败）
echo "\n\n" . str_repeat('#', 70) . "\n";
echo "步骤 8: 未登录状态创建技能（预期失败）\n";
echo str_repeat('#', 70) . "\n";

$response = httpRequest(BASE_URL . '/api/skill/create', 'POST', $functionSkillData);

$passed = printResult('未登录创建技能', $response, 0); // 预期返回错误码0
$testResults['no_login'] = $passed;

// 输出测试总结
echo "\n\n" . str_repeat('=', 70) . "\n";
echo "测试总结\n";
echo str_repeat('=', 70) . "\n";

$total = count($testResults);
$passedCount = array_sum($testResults);
$failCount = $total - $passedCount;

foreach ($testResults as $name => $result) {
    $status = $result ? '✓ PASS' : '✗ FAIL';
    echo "$status $name\n";
}

echo str_repeat('-', 70) . "\n";
echo "总计: $total | 通过: $passedCount | 失败: $failCount\n";
echo "成功率: " . round(($passedCount / $total) * 100, 2) . "%\n";

if ($createdSkillId) {
    echo "\n创建的技能ID: $createdSkillId\n";
}

echo str_repeat('=', 70) . "\n";

if ($failCount > 0) {
    exit(1);
} else {
    echo "\n✓ 所有测试通过！\n";
    exit(0);
}
