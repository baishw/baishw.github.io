<?php
/**
 * Auth认证类单元测试
 */

namespace tests\library;

use app\common\library\Auth;
use app\common\library\Token;
use app\common\model\User;
use fast\Random;
use think\Db;

class AuthTest extends \PHPUnit\Framework\TestCase
{
    /**
     * @var Auth
     */
    protected $auth;

    /**
     * @var array 测试用户数据
     */
    protected $testUser = [
        'username' => '',
        'password' => '',
        'email'    => '',
        'mobile'   => '',
    ];

    /**
     * 测试前设置
     */
    protected function setUp(): void
    {
        parent::setUp();
        
        // 初始化Auth实例
        $this->auth = Auth::instance();
        
        // 生成唯一测试用户
        $this->testUser = [
            'username' => 'test_user_' . Random::alnum(8),
            'password' => 'test_password_123',
            'email'    => 'test_' . Random::alnum(8) . '@example.com',
            'mobile'   => '1' . Random::numeric(10),
        ];

        // 开始事务，测试结束回滚
        Db::startTrans();
    }

    /**
     * 测试后清理
     */
    protected function tearDown(): void
    {
        // 回滚事务
        Db::rollback();
        
        // 重置Auth状态
        $this->auth->logout();
        
        parent::tearDown();
    }

    /**
     * 测试用户注册
     */
    public function testRegister()
    {
        $result = $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        $this->assertTrue($result, '注册应该成功');
        $this->assertNotNull($this->auth->getUser(), '注册后应该有用户对象');
        $this->assertEquals($this->testUser['username'], $this->auth->username, '用户名应该正确');
        $this->assertEquals($this->testUser['mobile'], $this->auth->mobile, '手机号应该正确');
        $this->assertEquals($this->testUser['email'], $this->auth->email, '邮箱应该正确');
        $this->assertNotEmpty($this->auth->getToken(), '注册后应该生成Token');
    }

    /**
     * 测试注册重复用户名
     */
    public function testRegisterDuplicateUsername()
    {
        // 先注册一个用户
        $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        // 尝试用相同用户名注册
        $result = $this->auth->register(
            $this->testUser['username'],
            'another_password',
            'another@example.com',
            '13900000000',
            []
        );

        $this->assertFalse($result, '重复用户名注册应该失败');
        $this->assertEquals('Username already exist', $this->auth->getError(), '错误信息应该正确');
    }

    /**
     * 测试账号密码登录
     */
    public function testLoginWithAccountPassword()
    {
        // 先注册用户
        $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        // 登出
        $this->auth->logout();

        // 使用用户名登录
        $result = $this->auth->login($this->testUser['username'], $this->testUser['password']);
        $this->assertTrue($result, '用户名登录应该成功');
        $this->assertEquals($this->testUser['username'], $this->auth->username);

        // 登出
        $this->auth->logout();

        // 使用邮箱登录
        $result = $this->auth->login($this->testUser['email'], $this->testUser['password']);
        $this->assertTrue($result, '邮箱登录应该成功');
        $this->assertEquals($this->testUser['email'], $this->auth->email);

        // 登出
        $this->auth->logout();

        // 使用手机号登录
        $result = $this->auth->login($this->testUser['mobile'], $this->testUser['password']);
        $this->assertTrue($result, '手机号登录应该成功');
        $this->assertEquals($this->testUser['mobile'], $this->auth->mobile);
    }

    /**
     * 测试错误密码登录
     */
    public function testLoginWithWrongPassword()
    {
        // 先注册用户
        $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        // 登出
        $this->auth->logout();

        // 使用错误密码登录
        $result = $this->auth->login($this->testUser['username'], 'wrong_password');
        $this->assertFalse($result, '错误密码登录应该失败');
        $this->assertEquals('Password is incorrect', $this->auth->getError(), '错误信息应该正确');
    }

    /**
     * 测试不存在的账号登录
     */
    public function testLoginWithNonExistentAccount()
    {
        $result = $this->auth->login('non_existent_user', 'password');
        $this->assertFalse($result, '不存在的账号登录应该失败');
        $this->assertEquals('Account is incorrect', $this->auth->getError(), '错误信息应该正确');
    }

    /**
     * 测试直接登录（通过用户ID）
     */
    public function testDirectLogin()
    {
        // 先注册用户
        $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        $userId = $this->auth->id;
        
        // 登出
        $this->auth->logout();

        // 使用用户ID直接登录
        $result = $this->auth->direct($userId);
        $this->assertTrue($result, '直接登录应该成功');
        $this->assertEquals($userId, $this->auth->id, '用户ID应该正确');
        $this->assertNotEmpty($this->auth->getToken(), '应该生成新的Token');
    }

    /**
     * 测试Token初始化
     */
    public function testTokenInit()
    {
        // 先注册用户获取Token
        $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        $token = $this->auth->getToken();
        $userId = $this->auth->id;

        // 创建新的Auth实例
        $newAuth = Auth::instance();

        // 使用Token初始化
        $result = $newAuth->init($token);
        $this->assertTrue($result, 'Token初始化应该成功');
        $this->assertEquals($userId, $newAuth->id, '用户ID应该正确');
        $this->assertEquals($token, $newAuth->getToken(), 'Token应该正确');
        $this->assertTrue($newAuth->isLogin(), '应该处于登录状态');
    }

    /**
     * 测试无效Token初始化
     */
    public function testInvalidTokenInit()
    {
        $invalidToken = 'invalid-token-12345';
        $result = $this->auth->init($invalidToken);
        $this->assertFalse($result, '无效Token初始化应该失败');
        $this->assertFalse($this->auth->isLogin(), '不应该处于登录状态');
    }

    /**
     * 测试退出登录
     */
    public function testLogout()
    {
        // 先注册并登录
        $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        $token = $this->auth->getToken();
        $this->assertTrue($this->auth->isLogin(), '登录后应该处于登录状态');

        // 退出登录
        $result = $this->auth->logout();
        $this->assertTrue($result, '退出应该成功');
        $this->assertFalse($this->auth->isLogin(), '退出后不应该处于登录状态');

        // 验证Token已被删除
        $tokenInfo = Token::get($token);
        $this->assertFalse($tokenInfo, 'Token应该已被删除');
    }

    /**
     * 测试未登录状态下退出
     */
    public function testLogoutWithoutLogin()
    {
        $result = $this->auth->logout();
        $this->assertFalse($result, '未登录状态下退出应该失败');
        $this->assertEquals('You are not logged in', $this->auth->getError(), '错误信息应该正确');
    }

    /**
     * 测试获取用户信息
     */
    public function testGetUserinfo()
    {
        // 先注册用户
        $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        $userinfo = $this->auth->getUserinfo();
        
        $this->assertIsArray($userinfo, '用户信息应该是数组');
        $this->assertEquals($this->testUser['username'], $userinfo['username'], '用户名应该正确');
        $this->assertEquals($this->testUser['nickname'] ?? $this->testUser['username'], $userinfo['nickname'], '昵称应该正确');
        $this->assertEquals($this->testUser['mobile'], $userinfo['mobile'], '手机号应该正确');
        $this->assertEquals($this->testUser['email'], $userinfo['email'], '邮箱应该正确');
        $this->assertArrayHasKey('token', $userinfo, '应该包含token字段');
        $this->assertArrayHasKey('expires_in', $userinfo, '应该包含expires_in字段');
    }

    /**
     * 测试修改密码
     */
    public function testChangePassword()
    {
        // 先注册用户
        $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        $userId = $this->auth->id;
        $oldToken = $this->auth->getToken();

        // 修改密码
        $newPassword = 'new_password_456';
        $result = $this->auth->changepwd($newPassword, $this->testUser['password']);
        $this->assertTrue($result, '修改密码应该成功');

        // 验证旧Token已失效
        $newAuth = Auth::instance();
        $result = $newAuth->init($oldToken);
        $this->assertFalse($result, '旧Token应该已失效');

        // 验证新密码可以登录
        $result = $newAuth->login($this->testUser['username'], $newPassword);
        $this->assertTrue($result, '新密码应该可以登录');
        $this->assertEquals($userId, $newAuth->id, '用户ID应该正确');
    }

    /**
     * 测试修改密码时旧密码错误
     */
    public function testChangePasswordWithWrongOldPassword()
    {
        // 先注册用户
        $this->auth->register(
            $this->testUser['username'],
            $this->testUser['password'],
            $this->testUser['email'],
            $this->testUser['mobile'],
            []
        );

        // 使用错误的旧密码修改
        $result = $this->auth->changepwd('new_password', 'wrong_old_password');
        $this->assertFalse($result, '旧密码错误时修改应该失败');
        $this->assertEquals('Password is incorrect', $this->auth->getError(), '错误信息应该正确');
    }

    /**
     * 测试获取加密密码
     */
    public function testGetEncryptPassword()
    {
        $password = 'test_password';
        $salt = 'random_salt';
        
        // 测试加密
        $encrypted = $this->auth->getEncryptPassword($password, $salt);
        
        // 验证格式
        $this->assertEquals(32, strlen($encrypted), '加密后的密码应该是32位MD5');
        
        // 验证相同输入产生相同输出
        $encrypted2 = $this->auth->getEncryptPassword($password, $salt);
        $this->assertEquals($encrypted, $encrypted2, '相同输入应该产生相同输出');
        
        // 验证不同输入产生不同输出
        $encrypted3 = $this->auth->getEncryptPassword('different_password', $salt);
        $this->assertNotEquals($encrypted, $encrypted3, '不同密码应该产生不同输出');
        
        $encrypted4 = $this->auth->getEncryptPassword($password, 'different_salt');
        $this->assertNotEquals($encrypted, $encrypted4, '不同盐应该产生不同输出');
    }

    /**
     * 测试match方法
     */
    public function testMatch()
    {
        // 测试匹配
        $result = $this->auth->match(['login', 'register']);
        // 需要模拟请求
        $this->markTestIncomplete('需要模拟请求才能测试match方法');
    }
}