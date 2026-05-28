<?php
/**
 * User API控制器集成测试
 */

namespace tests\api;

use app\api\controller\User;
use app\common\model\User as UserModel;
use fast\Random;
use think\Config;
use think\Request;
use think\Response;

class UserApiTest extends \PHPUnit\Framework\TestCase
{
    /**
     * @var User
     */
    protected $controller;

    /**
     * @var Request
     */
    protected $request;

    /**
     * @var array 测试用户数据
     */
    protected $testUser = [];

    /**
     * @var string 登录后获取的Token
     */
    protected $token;

    /**
     * 测试前设置
     */
    protected function setUp(): void
    {
        parent::setUp();

        // 重置配置
        Config::set('token', [
            'type'   => 'File',
            'expire' => 2592000,
        ]);

        // 生成唯一测试用户
        $this->testUser = [
            'username' => 'test_api_user_' . Random::alnum(8),
            'password' => 'test_password_123',
            'email'    => 'test_api_' . Random::alnum(8) . '@example.com',
            'mobile'   => '1' . Random::numeric(10),
        ];

        // 创建请求实例
        $this->request = Request::instance();
    }

    /**
     * 测试后清理
     */
    protected function tearDown(): void
    {
        // 如果有登录的Token，尝试登出
        if ($this->token) {
            try {
                $this->request->header(['Token' => $this->token]);
                $this->request->method('POST');
                $controller = new User($this->request);
                $controller->logout();
            } catch (\Exception $e) {
                // 忽略登出异常
            }
        }

        // 删除测试用户
        if (!empty($this->testUser['username'])) {
            $user = UserModel::getByUsername($this->testUser['username']);
            if ($user) {
                $user->delete();
            }
        }

        parent::tearDown();
    }

    /**
     * 模拟请求并获取响应
     */
    protected function mockRequest($method, $data = [], $token = null)
    {
        $this->request->method($method);
        
        if ($token) {
            $this->request->header(['Token' => $token]);
        }

        if ($method === 'POST') {
            $this->request->post($data);
        } else {
            $this->request->get($data);
        }

        return $this->request;
    }

    /**
     * 解析JSON响应
     */
    protected function parseJsonResponse($response)
    {
        if ($response instanceof Response) {
            $content = $response->getContent();
            return json_decode($content, true);
        }
        return null;
    }

    /**
     * 测试注册接口
     */
    public function testRegister()
    {
        $this->mockRequest('POST', [
            'username' => $this->testUser['username'],
            'password' => $this->testUser['password'],
            'email'    => $this->testUser['email'],
            'mobile'   => $this->testUser['mobile'],
            'code'     => '123456', // 模拟验证码
        ]);

        // 由于需要验证码验证，这里测试参数验证失败的情况
        $controller = new User($this->request);
        
        // 测试参数缺失的情况
        $this->request->post(['username' => '', 'password' => '']);
        try {
            $response = $controller->register();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(0, $result['code'], '参数缺失应该返回错误码0');
            $this->assertEquals('Invalid parameters', $result['msg'], '错误信息应该正确');
        }
    }

    /**
     * 测试登录接口（账号密码登录）
     */
    public function testLogin()
    {
        // 先创建测试用户
        $user = UserModel::create([
            'username' => $this->testUser['username'],
            'password' => md5(md5($this->testUser['password']) . 'testsalt'),
            'salt'     => 'testsalt',
            'email'    => $this->testUser['email'],
            'mobile'   => $this->testUser['mobile'],
            'status'   => 'normal',
            'nickname' => $this->testUser['username'],
            'jointime' => time(),
            'logintime' => time(),
            'joinip'   => '127.0.0.1',
            'loginip'  => '127.0.0.1',
        ]);

        // 测试登录
        $this->mockRequest('POST', [
            'account'  => $this->testUser['username'],
            'password' => $this->testUser['password'],
        ]);

        $controller = new User($this->request);
        
        try {
            $response = $controller->login();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(1, $result['code'], '登录成功应该返回码1');
            $this->assertEquals('Logged in successful', $result['msg'], '成功信息应该正确');
            $this->assertArrayHasKey('userinfo', $result['data'], '应该包含用户信息');
            $this->assertEquals($this->testUser['username'], $result['data']['userinfo']['username'], '用户名应该正确');
            $this->assertArrayHasKey('token', $result['data']['userinfo'], '应该包含token');
            
            // 保存Token供后续测试使用
            $this->token = $result['data']['userinfo']['token'];
        }
    }

    /**
     * 测试登录接口（错误密码）
     */
    public function testLoginWithWrongPassword()
    {
        // 先创建测试用户
        UserModel::create([
            'username' => $this->testUser['username'],
            'password' => md5(md5($this->testUser['password']) . 'testsalt'),
            'salt'     => 'testsalt',
            'email'    => $this->testUser['email'],
            'mobile'   => $this->testUser['mobile'],
            'status'   => 'normal',
            'nickname' => $this->testUser['username'],
            'jointime' => time(),
            'logintime' => time(),
            'joinip'   => '127.0.0.1',
            'loginip'  => '127.0.0.1',
        ]);

        // 测试错误密码登录
        $this->mockRequest('POST', [
            'account'  => $this->testUser['username'],
            'password' => 'wrong_password',
        ]);

        $controller = new User($this->request);
        
        try {
            $response = $controller->login();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(0, $result['code'], '错误密码应该返回码0');
            $this->assertEquals('Password is incorrect', $result['msg'], '错误信息应该正确');
        }
    }

    /**
     * 测试登录接口（不存在的账号）
     */
    public function testLoginWithNonExistentAccount()
    {
        $this->mockRequest('POST', [
            'account'  => 'non_existent_user',
            'password' => 'password',
        ]);

        $controller = new User($this->request);
        
        try {
            $response = $controller->login();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(0, $result['code'], '不存在的账号应该返回码0');
            $this->assertEquals('Account is incorrect', $result['msg'], '错误信息应该正确');
        }
    }

    /**
     * 测试退出登录接口
     */
    public function testLogout()
    {
        // 先创建用户并登录
        $user = UserModel::create([
            'username' => $this->testUser['username'],
            'password' => md5(md5($this->testUser['password']) . 'testsalt'),
            'salt'     => 'testsalt',
            'email'    => $this->testUser['email'],
            'mobile'   => $this->testUser['mobile'],
            'status'   => 'normal',
            'nickname' => $this->testUser['username'],
            'jointime' => time(),
            'logintime' => time(),
            'joinip'   => '127.0.0.1',
            'loginip'  => '127.0.0.1',
        ]);

        // 先登录获取Token
        $this->mockRequest('POST', [
            'account'  => $this->testUser['username'],
            'password' => $this->testUser['password'],
        ]);

        $controller = new User($this->request);
        
        try {
            $controller->login();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->token = $result['data']['userinfo']['token'];
        }

        // 测试退出登录
        $this->mockRequest('POST', [], $this->token);
        
        try {
            $response = $controller->logout();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(1, $result['code'], '退出成功应该返回码1');
            $this->assertEquals('Logout successful', $result['msg'], '成功信息应该正确');
        }
    }

    /**
     * 测试会员中心接口（需要登录）
     */
    public function testIndex()
    {
        // 先创建用户并登录
        $user = UserModel::create([
            'username' => $this->testUser['username'],
            'password' => md5(md5($this->testUser['password']) . 'testsalt'),
            'salt'     => 'testsalt',
            'email'    => $this->testUser['email'],
            'mobile'   => $this->testUser['mobile'],
            'status'   => 'normal',
            'nickname' => '测试昵称',
            'jointime' => time(),
            'logintime' => time(),
            'joinip'   => '127.0.0.1',
            'loginip'  => '127.0.0.1',
        ]);

        // 先登录获取Token
        $this->mockRequest('POST', [
            'account'  => $this->testUser['username'],
            'password' => $this->testUser['password'],
        ]);

        $controller = new User($this->request);
        
        try {
            $controller->login();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->token = $result['data']['userinfo']['token'];
        }

        // 测试会员中心
        $this->mockRequest('GET', [], $this->token);
        
        try {
            $response = $controller->index();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(1, $result['code'], '会员中心应该返回码1');
            $this->assertEquals('测试昵称', $result['data']['welcome'], '欢迎信息应该包含昵称');
        }
    }

    /**
     * 测试会员中心接口（未登录）
     */
    public function testIndexWithoutLogin()
    {
        $this->mockRequest('GET', []);
        
        $controller = new User($this->request);
        
        try {
            $response = $controller->index();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(0, $result['code'], '未登录应该返回码0');
            $this->assertEquals('Please login first', $result['msg'], '错误信息应该正确');
        }
    }
}