### 1. 在Xcode中将scheme设为共享
点击`Project->Scheme->Edit Scheme`， 勾选`Shared`。

### 2. 提供如下信息

|项目 |说明|
|----|----|
|Workspace|xxx.xcworkspace文件|
|Project|xxx.xcodeproj文件|
|Scheme|在第一步操作完成后可以通过命令`xcodebuild -list`查看|
|SDK|通过命令`xcodebuild -showsdks`|
|代码目录 |项目的主要代码目录|
|第三方代码目录 |第三方代码目录，比如Cocoapod管理的第三方代码都在Pod目录下，这些代码不需要进行分析。另外还有直接引入项目中的第三方代码目录。|


#### 示例

|项目 |说明|
|----|----|
|Workspace|AFNetworking.xcworkspace|
|Project|AFNetworking.xcodeproj|
|Scheme|AFNetworking iOS|
|SDK|iphonesimulator11.1|
|代码目录 |AFNetworking|
|第三方代码目录 |Pod|

### 3. 检查
整理好上述信息后可以在项目目录下执行如下命令：

    xcodebuild -workspace AFNetworking.xcworkspace -scheme AFNetworking\ iOS -sdk iphonesimulator11.0 -configuration Debug

> 注意将上面命令中的workspace，scheme，sdk替换为自己项目。注意如果scheme或其它参数中有空格，需要用`\`转义。

如果可以编译成功即表示信息无误。


### 4. 特别说明
由于主要进行代码分析，不涉及打包流程，最好确保项目可以使用iOS Simulator SDKs进行编译。另外尽量使用比较新的Xcode及SDK编译。
