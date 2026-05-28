<?php
/**
 * 单元测试引导文件
 */
define('APP_PATH', realpath(__DIR__ . '/../application/'));
define('ROOT_PATH', realpath(__DIR__ . '/../'));

// 加载框架入口
require ROOT_PATH . '/thinkphp/start.php';

// 设置测试环境配置
\think\Config::load(ROOT_PATH . '/application/database-develope.php', 'database');

// 关闭严格模式以便测试
error_reporting(E_ALL & ~E_NOTICE & ~E_STRICT);

// 注册自动加载
spl_autoload_register(function ($class) {
    $class = str_replace('\\', '/', $class);
    $file = ROOT_PATH . '/tests/' . $class . '.php';
    if (is_file($file)) {
        require $file;
    }
});