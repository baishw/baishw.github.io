<?php
/**
 * 测试网站：https://skill.cxus.cn
 * 测试账号：skillpuber
 * 密码：123456
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
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
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

    echo "\n" . str_repeat('=', 60) . "\n";
    echo "$status 测试: $testName\n";
    echo str_repeat('-', 60) . "\n";

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

// ==================== 测试用例 ====================

echo "\n";
echo str_repeat('*', 60) . "\n";
echo "* 技能平台 API 测试\n";
echo "* 测试网站: " . BASE_URL . "\n";
echo "* 测试账号: " . TEST_ACCOUNT . "\n";
echo "* 时间: " . date('Y-m-d H:i:s') . "\n";
echo str_repeat('*', 60) . "\n";

$testResults = [];
$token = '';

// 测试1: 登录接口
echo "\n\n" . str_repeat('#', 60) . "\n";
echo "测试 1: 用户登录\n";
echo str_repeat('#', 60) . "\n";

$response = httpRequest(BASE_URL . '/api/user/login', 'POST', [
    'account' => TEST_ACCOUNT,
    'password' => TEST_PASSWORD
]);

$passed = printResult('账号密码登录', $response, 1);
$testResults['login'] = $passed;

if ($passed && isset($response['decoded']['data']['userinfo']['token'])) {
    $token = $response['decoded']['data']['userinfo']['token'];
    echo "\n  获取到Token: " . substr($token, 0, 20) . "...\n";
    echo "  用户昵称: " . ($response['decoded']['data']['userinfo']['nickname'] ?? '未知') . "\n";
}

// 测试2: 会员中心（需要登录）
echo "\n\n" . str_repeat('#', 60) . "\n";
echo "测试 2: 访问会员中心（需要Token）\n";
echo str_repeat('#', 60) . "\n";

$response = httpRequest(BASE_URL . '/api/user/index', 'GET', [], [
    'Token' => $token
]);

$passed = printResult('会员中心', $response, 1);
$testResults['user_index'] = $passed;

// 测试3: Token检查接口
echo "\n\n" . str_repeat('#', 60) . "\n";
echo "测试 3: Token检查接口\n";
echo str_repeat('#', 60) . "\n";

$response = httpRequest(BASE_URL . '/api/token/check', 'GET', [], [
    'Token' => $token
]);

$passed = printResult('Token检查', $response, 1);
$testResults['token_check'] = $passed;

// 测试4: Token刷新接口
echo "\n\n" . str_repeat('#', 60) . "\n";
echo "测试 4: Token刷新接口\n";
echo str_repeat('#', 60) . "\n";

$response = httpRequest(BASE_URL . '/api/token/refresh', 'GET', [], [
    'Token' => $token
]);

$passed = printResult('Token刷新', $response, 1);
$testResults['token_refresh'] = $passed;

if ($passed && isset($response['decoded']['data']['token'])) {
    $newToken = $response['decoded']['data']['token'];
    echo "\n  新Token: " . substr($newToken, 0, 20) . "...\n";
    echo "  Token是否变化: " . ($token !== $newToken ? '是' : '否') . "\n";
    $token = $newToken; // 使用新Token继续测试
}

// 测试5: 退出登录
echo "\n\n" . str_repeat('#', 60) . "\n";
echo "测试 5: 退出登录\n";
echo str_repeat('#', 60) . "\n";

$response = httpRequest(BASE_URL . '/api/user/logout', 'POST', [], [
    'Token' => $token
]);

$passed = printResult('退出登录', $response, 1);
$testResults['logout'] = $passed;

// 测试6: 退出后访问会员中心（应失败）
echo "\n\n" . str_repeat('#', 60) . "\n";
echo "测试 6: 退出后访问会员中心（验证Token失效）\n";
echo str_repeat('#', 60) . "\n";

$response = httpRequest(BASE_URL . '/api/user/index', 'GET', [], [
    'Token' => $token
]);

$passed = printResult('退出后访问会员中心', $response, 0); // 应该返回错误码0
$testResults['logout_verify'] = $passed;

// 测试7: 未登录状态访问会员中心
echo "\n\n" . str_repeat('#', 60) . "\n";
echo "测试 7: 未登录状态访问会员中心\n";
echo str_repeat('#', 60) . "\n";

$response = httpRequest(BASE_URL . '/api/user/index', 'GET');

$passed = printResult('未登录访问会员中心', $response, 0); // 应该返回错误码0
$testResults['no_login_access'] = $passed;

// 测试8: 获取技能列表
echo "\n\n" . str_repeat('#', 60) . "\n";
echo "测试 8: 获取技能列表\n";
echo str_repeat('#', 60) . "\n";

$response = httpRequest(BASE_URL . '/api/skill/index');

$passed = printResult('获取技能列表', $response, 1);
$testResults['skill_index'] = $passed;

// 输出测试总结
echo "\n\n" . str_repeat('=', 60) . "\n";
echo "测试总结\n";
echo str_repeat('=', 60) . "\n";

$total = count($testResults);
$passedCount = array_sum($testResults);
$failCount = $total - $passedCount;

foreach ($testResults as $name => $result) {
    $status = $result ? '✓ PASS' : '✗ FAIL';
    echo "$status $name\n";
}

echo str_repeat('-', 60) . "\n";
echo "总计: $total | 通过: $passedCount | 失败: $failCount\n";
echo "成功率: " . round(($passedCount / $total) * 100, 2) . "%\n";
echo str_repeat('=', 60) . "\n";

if ($failCount > 0) {
    exit(1);
} else {
    echo "\n✓ 所有测试通过！\n";
    exit(0);
}
