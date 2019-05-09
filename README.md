# xuexi.cn

学习强国积分自动获取，模拟手动操作

## 说明

- 建议有一定python基础（~~都python了还需要个锤子的基础~~）
- python3 + selenium
- 仅限学习交流使用

## 工作环境

1. windows操作系统
2. 最新版chrom浏览器
3. python3

## 配置工作

1. 安装第三方库selenium

2. 将chromedriver目录下的chromedriver.exe文件配置到系统路径

   ```
   # 我的电脑 -> 属性 -> 高级系统设置 -> 环境变量 -> 系统变量
   # 在系统变量中的path中添加
   # 如我的路径是：D:\xuexi.cn\chromedriver\chromedriver.exe
   ```

3. 将chromedriver.exe的路径配置到config.py中

   ```
   # 用户配置：chromedriver.exe文件地址
   USER_CONFIG = {
   	"chrome_driver": "xxx",
   	# 如我的地址是
   	# "chrome_driver": r"D:\xuexi.cn\chromedriver\chromedriver.exe",
   }
   ```

## 使用说明

**双击执行.bat文件即可**

