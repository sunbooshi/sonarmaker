### 项目说明

####更新：
提供了编译好的配置工具，请[点击下载v0.1](https://github.com/sunboshi/sonarmaker/releases/download/v0.1/sonarmaker-0.1.zip)，直接运行`start`脚本，会使用python启动一个简单的WebServer。

在浏览器中访问[http://localhost:9090](http://localhost:9090)即可使用配置工具。

------------

为iOS工程进行代码分析生成配置文件，配合`jenkins-sonar.py`脚本可以实现自动化生成分析报告。

详细过程请参考以下两篇文章：

[《使用Jenkins+OCLint+SonarCube对iOS项目进行代码分析》](http://www.sunboshi.tech/2018/03/27/jekins-oclint-sonarcube/)

[《批量化的项目代码分析脚本及配置工具》](http://www.sunboshi.tech/2018/03/29/oclint-python/)


可以部署到服务器，也可以作为Chrome App独立运行。由于Chrome App即将终止，所以之后只能在网页里使用了。

由于使用来vue.js，所以需要安装node.js及npm。具体安装方式请参考：

[node.js安装](https://nodejs.org/en/download/package-manager/#macos)

[npm安装](https://www.npmjs.com/package/npm)

使用如下命令来启动配置工具：
``` bash
# 安装依赖
npm install

# 在8080端口启动开发服务
npm run dev

# 以下命令用于部署
# 生成发布版本
npm run build

# 生成chrome app
./buildchromeapp
```
执行`./buildchromeapp`后，将chrome目录就可以作为chrome app启动了。因为最新的chrome已经终止了对chrome app的支持，所以不推荐使用。

### jenkins-sonar.py使用指南
`jenkins-sonar.py`主要配合Jenkins来使用，另外也可以配合Mac的定时任务独立使用。
使用方式如下：

    # 直接编译工程，project.json是通过配置工具生成的项目配置
    jenkins-sonar.py project.json

    # -test 测试配置文件，并不编译，可以通过该方式检查项目
    jenkins-sonar.py project.json -test

    # -git 使用git，主要用于配合定时任务独立使用，使用该参数时配置文件中的git仓库一项有效
    jenkins-sonar.py project.json


采用定时任务具体步骤请参考`crontab.md`。

关于配置工具配置项的说明请参考`sonarproject.md`。

`AFNetworking.json`是用配置工具生成的项目配置文件示例。

`cn.oc.sonar.afnetwroking.plist`是定时任务plist示例。
