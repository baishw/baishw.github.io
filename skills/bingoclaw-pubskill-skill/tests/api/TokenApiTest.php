<?php
/**
 * Token API控制器集成测试
 */

namespace tests\api;

use app\api\controller\Token;
use app\common\library\Token as TokenLib;
use app\common\model\User as UserModel;
use fast\Random;
use think\Request;

class TokenApiTest extends \PHPUnit\Framework\TestCase
{
    /**
     * @var Request
     */
    protected $request;

    /**
     * @var string 测试用的Token
     */
    protected $token;

    /**
     * 测试前设置
     */
    protected function setUp(): void
    {
        parent::setUp();

        // 创建请求实例
        $this->request = Request::instance();

        // 创建测试用户并获取Token
        $username = 'test_token_user_' . Random::alnum(8);
        $password = 'test_password_123';
        
        $user = UserModel::create([
            'username' => $username,
            'password' => md5(md5($password) . 'testsalt'),
            'salt'     => 'testsalt',
            'email'    => 'test_' . Random::alnum(8) . '@example.com',
            'mobile'   => '1' . Random::numeric(10),
            'status'   => 'normal',
            'nickname' => $username,
            'jointime' => time(),
            'logintime' => time(),
            'joinip'   => '127.0.0.1',
            'loginip'  => '127.0.0.1',
        ]);

        // 生成Token
        $this->token = Random::uuid();
        TokenLib::set($this->token, $user->id, 2592000);
    }

    /**
     * 测试后清理
     */
    protected function tearDown(): void
    {
        // 删除测试Token
        if ($this->token) {
            TokenLib::delete($this->token);
        }
        parent::tearDown();
    }

    /**
     * 解析JSON响应
     */
    protected function parseJsonResponse($response)
    {
        if ($response instanceof \think\Response) {
            $content = $response->getContent();
            return json_decode($content, true);
        }
        return null;
    }

    /**
     * 测试Token检查接口
     */
    public function testCheckToken()
    {
        $this->request->header(['Token' => $this->token]);
        $this->request->method('GET');

        $controller = new Token($this->request);

        try {
            $response = $controller->check();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(1, $result['code'], 'Token检查应该成功');
            $this->assertEquals($this->token, $result['data']['token'], 'Token值应该正确');
            $this->assertArrayHasKey('expires_in', $result['data'], '应该包含过期时间');
        }
    }

    /**
     * 测试Token刷新接口
     */
    public function testRefreshToken()
    {
        $oldToken = $this->token;
        
        $this->request->header(['Token' => $oldToken]);
        $this->request->method('GET');

        $controller = new Token($this->request);

        try {
            $response = $controller->refresh();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(1, $result['code'], 'Token刷新应该成功');
            $this->assertNotEmpty($result['data']['token'], '应该返回新Token');
            $this->assertNotEquals($oldToken, $result['data']['token'], '新Token应该与旧Token不同');
            $this->assertEquals(2592000, $result['data']['expires_in'], '过期时间应该正确');

            // 验证旧Token已失效
            $oldTokenInfo = TokenLib::get($oldToken);
            $this->assertFalse($oldTokenInfo, '旧Token应该已失效');

            // 验证新Token有效
            $newToken = $result['data']['token'];
            $newTokenInfo = TokenLib::get($newToken);
            $this->assertNotNull($newTokenInfo, '新Token应该有效');
            $this->assertEquals($newToken, $newTokenInfo['token'], '新Token信息应该正确');
        }
    }

    /**
     * 测试Token检查接口（无效Token）
     */
    public function testCheckInvalidToken()
    {
        $this->request->header(['Token' => 'invalid_token_123']);
        $this->request->method('GET');

        $controller = new Token($this->request);

        try {
            $response = $controller->check();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(0, $result['code'], '无效Token应该返回错误');
            $this->assertEquals('Please login first', $result['msg'], '错误信息应该正确');
        }
    }

    /**
     * 测试Token刷新接口（无效Token）
     */
    public function testRefreshInvalidToken()
    {
        $this->request->header(['Token' => 'invalid_token_123']);
        $this->request->method('GET');

        $controller = new Token($this->request);

        try {
            $response = $controller->refresh();
        } catch (\think\exception\HttpResponseException $e) {
            $result = $this->parseJsonResponse($e->getResponse());
            $this->assertEquals(0, $result['code'], '无效Token刷新应该失败');
            $this->assertEquals('Please login first', $result['msg'], '错误信息应该正确');
        }
    }
}