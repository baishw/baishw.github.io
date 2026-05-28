<?php
/**
 * Token操作类单元测试
 */

namespace tests\library;

use app\common\library\Token;
use fast\Random;
use think\Config;

class TokenTest extends \PHPUnit\Framework\TestCase
{
    /**
     * @var string 测试用的Token
     */
    protected $testToken;

    /**
     * @var int 测试用的用户ID
     */
    protected $testUserId = 1;

    /**
     * 测试前设置
     */
    protected function setUp(): void
    {
        parent::setUp();
        
        // 生成唯一Token
        $this->testToken = Random::uuid();
    }

    /**
     * 测试后清理
     */
    protected function tearDown(): void
    {
        // 清理测试数据
        Token::delete($this->testToken);
        parent::tearDown();
    }

    /**
     * 测试设置Token
     */
    public function testSetToken()
    {
        $result = Token::set($this->testToken, $this->testUserId, 3600);
        $this->assertTrue($result, '设置Token应该成功');
    }

    /**
     * 测试获取Token
     */
    public function testGetToken()
    {
        // 先设置Token
        Token::set($this->testToken, $this->testUserId, 3600);

        // 获取Token信息
        $tokenInfo = Token::get($this->testToken);
        
        $this->assertNotNull($tokenInfo, '获取Token信息应该成功');
        $this->assertIsArray($tokenInfo, 'Token信息应该是数组');
        $this->assertEquals($this->testToken, $tokenInfo['token'], 'Token值应该正确');
        $this->assertEquals($this->testUserId, $tokenInfo['user_id'], '用户ID应该正确');
        $this->assertArrayHasKey('expires_in', $tokenInfo, '应该包含过期时间');
        $this->assertEquals(3600, $tokenInfo['expires_in'], '过期时间应该正确');
    }

    /**
     * 测试获取不存在的Token
     */
    public function testGetNonExistentToken()
    {
        $tokenInfo = Token::get('non_existent_token');
        $this->assertFalse($tokenInfo, '获取不存在的Token应该返回false');
    }

    /**
     * 测试删除Token
     */
    public function testDeleteToken()
    {
        // 先设置Token
        Token::set($this->testToken, $this->testUserId, 3600);

        // 验证Token存在
        $tokenInfo = Token::get($this->testToken);
        $this->assertNotNull($tokenInfo, 'Token应该存在');

        // 删除Token
        $result = Token::delete($this->testToken);
        $this->assertTrue($result, '删除Token应该成功');

        // 验证Token已删除
        $tokenInfo = Token::get($this->testToken);
        $this->assertFalse($tokenInfo, '删除后Token应该不存在');
    }

    /**
     * 测试验证Token
     */
    public function testCheckToken()
    {
        // 先设置Token
        Token::set($this->testToken, $this->testUserId, 3600);

        // 验证Token
        $result = Token::check($this->testToken, $this->testUserId);
        $this->assertTrue($result, 'Token验证应该成功');

        // 验证错误的用户ID
        $result = Token::check($this->testToken, 999);
        $this->assertFalse($result, '错误用户ID验证应该失败');

        // 验证不存在的Token
        $result = Token::check('non_existent', $this->testUserId);
        $this->assertFalse($result, '不存在的Token验证应该失败');
    }

    /**
     * 测试has方法（check别名）
     */
    public function testHasToken()
    {
        // 先设置Token
        Token::set($this->testToken, $this->testUserId, 3600);

        // 测试has方法
        $result = Token::has($this->testToken, $this->testUserId);
        $this->assertTrue($result, 'has方法应该返回true');
    }

    /**
     * 测试rm方法（delete别名）
     */
    public function testRmToken()
    {
        // 先设置Token
        Token::set($this->testToken, $this->testUserId, 3600);

        // 测试rm方法
        $result = Token::rm($this->testToken);
        $this->assertTrue($result, 'rm方法应该成功删除Token');

        // 验证Token已删除
        $tokenInfo = Token::get($this->testToken);
        $this->assertFalse($tokenInfo, '删除后Token应该不存在');
    }

    /**
     * 测试Token过期
     */
    public function testTokenExpiration()
    {
        // 设置一个短过期时间的Token（1秒）
        Token::set($this->testToken, $this->testUserId, 1);

        // 立即验证应该有效
        $result = Token::check($this->testToken, $this->testUserId);
        $this->assertTrue($result, '刚设置的Token应该有效');

        // 等待2秒让Token过期
        sleep(2);

        // 再次验证应该无效
        $result = Token::check($this->testToken, $this->testUserId);
        $this->assertFalse($result, '过期的Token应该无效');
    }

    /**
     * 测试批量操作多个Token
     */
    public function testMultipleTokens()
    {
        $token1 = Random::uuid();
        $token2 = Random::uuid();
        $userId1 = 100;
        $userId2 = 200;

        // 设置两个不同用户的Token
        Token::set($token1, $userId1, 3600);
        Token::set($token2, $userId2, 3600);

        // 验证各自的Token
        $info1 = Token::get($token1);
        $info2 = Token::get($token2);
        
        $this->assertEquals($userId1, $info1['user_id'], '第一个Token的用户ID应该正确');
        $this->assertEquals($userId2, $info2['user_id'], '第二个Token的用户ID应该正确');

        // 删除第一个Token
        Token::delete($token1);
        $this->assertFalse(Token::get($token1), '第一个Token应该已删除');
        $this->assertNotNull(Token::get($token2), '第二个Token应该仍然存在');

        // 清理
        Token::delete($token2);
    }

    /**
     * 测试Token配置初始化
     */
    public function testTokenInitWithConfig()
    {
        // 获取默认配置
        $config = Config::get('token');
        
        $this->assertNotEmpty($config, 'Token配置应该存在');
        $this->assertArrayHasKey('type', $config, '配置应该包含type字段');
    }
}