# 新浪微博爬虫使用说明

#### 环境配置

- 首先进入项目src文件夹下，执行`source env.sh`命令，若已经入虚拟环境中说明生效：

  ```
  jhchen:src jhchen$ source env.sh 
  (sinaspider)jhchen:src jhchen$ 
  ```

- 返回至上级目录，进入pip文件夹下，执行`sh install.sh`安装所需要的依赖包

- 数据库使用的为MySQL，初始化数据库脚本，进入scripts目录，运行脚本，如下：

  ```
  (sinaspider)jhchen:SinaSpider jhchen$ ls
  
  docs pip  src
  
  (sinaspider)jhchen:SinaSpider jhchen$ cd src/scripts/
  
  (sinaspider)jhchen:scripts jhchen$ sh init-mysql.sh 
  (sinaspider)jhchen:scripts jhchen$ sh init-table.sh 
  删除ss_sina_user表
  删除完毕
  创建ss_sina_user表
  创建完成
  ```

#### 项目运行

- 安装好依赖后，执行测试脚本main_test.py即可运行
