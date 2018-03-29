# 项目部署

### 1. 安装OCLint(0.13.1)
从这里下载0.13.1版本的压缩包
https://github.com/oclint/oclint/releases

将OCLint添加至PATH

### 2. 安装XCPretty(0.28)
使用如下命令安装

    gem install xcpretty

### 3. 安装Sonar-Scanner
从这里下载安装包
https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner

将Sonar-Scanner添加至PATH

### 4. 创建定时任务

1) 修改cn.oc.sonar.plist，将文件名改为cn.oc.sonar.项目名称.plist。

2) 修改Label值为cn.oc.sonar.项目名称,需要保证唯一性。

3) 修改Program路径

4) 修改ProgramArguments

5) 修改WorkingDirectory路径

6) 修改StandardOutPath路径

7) 修改StandardErrorPath路径

8) 将plist文件拷贝至~/Library/LaunchAgents/


    cp cn.oc.sonar.afnetwroking.plist ~/Library/LaunchAgents/

使用如下命令启动定时任务

a) 设置PATH变量

    launchctl setenv PATH $PATH  

b) 启动定时任务

    launchctl load cn.oc.sonar.afnetwroking.plist

c）停止定时任务

    launchctl unload cn.oc.sonar.afnetwroking.plist
