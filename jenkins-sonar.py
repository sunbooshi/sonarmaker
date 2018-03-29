#!/usr/bin/python
# encoding:utf8

import os
import json
import sys
import logging
import xml.etree.ElementTree as ET

Verison = '0.1.0'
isTest = False
useGit = False

workpath = 'project'

def runCmd(cmd):
    if isTest:
        print cmd
        return 0
    else:
        return os.system(cmd)

def replaceSpace(p):
    # 处理参数中的空格
    return p.replace(' ', '\ ')

class Project:
    def __init__(self, jsonData):
        self.git = jsonData['git']
        self.branch = jsonData['branch']
        self.workspace = jsonData['workspace']
        self.project = jsonData['project']
        self.scheme = jsonData['scheme']
        self.sdk = jsonData['sdk']
        self.src = jsonData['src']
        self.buildResult = False

    def clone(self):
        if not os.path.isdir(os.path.join(os.getcwd(), workpath)):
            runCmd('git clone ' + self.git + ' ' + workpath)

    def checkout(self):
        runCmd('git checkout ' + self.branch)

    def pull(self):
        runCmd('git pull')

    def makeCmd(self):
        fmt = 'xcodebuild -workspace %s -scheme %s -sdk %s -configuration Debug '
        return fmt % (replaceSpace(self.workspace), replaceSpace(self.scheme), replaceSpace(self.sdk))

    def build(self):
        build = 'COMPILER_INDEX_STORE_ENABLE=NO | tee xcodebuild.log | xcpretty -r json-compilation-database -o compile_commands.json'
        cmd = self.makeCmd() + build
        self.buildResult = runCmd(cmd)

    def clean(self):
        cmd = self.makeCmd() + 'clean'
        runCmd(cmd)

    def isSuccess(self):
        # 这里xcpretty没有返回状态
        # return self.buildResult and os.path.exists(os.path.join(os.getcwd(), workpath, 'compile_commands.json'))
        return os.path.exists(os.path.join(os.getcwd(), 'compile_commands.json'))

class OClint():
    def __init__(self, jsonData):
        self.exclude = jsonData['exclude']
        self.longLine = jsonData['longLine']
        self.longMethod = jsonData['longMethod']
        self.disableRules = jsonData['disableRules']
        self.cyclomaticComplexity = jsonData['cyclomaticComplexity']
        self.longVariableName = jsonData['longVariableName']

    def genConfig(self):
        fp = open('.oclint', 'w')

        fp.write('rule-configurations:\n')
        fp.write('  - key: LONG_LINE\n')
        fp.write('    value: %s\n' % self.longLine)
        fp.write('  - key: LONG_METHOD\n')
        fp.write('    value: %s\n' % self.longMethod)
        fp.write('  - key: CYCLOMATIC_COMPLEXITY\n')
        fp.write('    value: %s\n' % self.cyclomaticComplexity)
        fp.write('  - key: LONG_VARIABLE_NAME\n')
        fp.write('    value: %s\n' % self.longVariableName)
        fp.write('\n')

        fp.write('disable-rules:\n')
        for rule in self.disableRules:
            fp.write('  - %s\n' % rule)
        fp.write('\n')

        fp.write('report-type: pmd\n')
        fp.write('output: oclint.xml\n')
        fp.write('max-priority-1: 10000\n')
        fp.write('max-priority-2: 10000\n')
        fp.write('max-priority-3: 10000\n')
        fp.write('enable-clang-static-analyzer: false\n')

        fp.close()

    def run(self):
        self.genConfig()
        excludeDirs = ''.join(['-e ' + x + ' ' for x in self.exclude.split(',')])
        runCmd('oclint-json-compilation-database ' + excludeDirs)

    def isSuccess(self):
        r1 = os.path.exists(os.path.join(os.getcwd(), 'oclint.xml'))
        r2 = os.path.exists(os.path.join(os.getcwd(), 'oclint.xml.origin'))
        return r1 and r2

    def rmClangRules(self):
        result = os.system('mv oclint.xml oclint.xml.origin')
        if (result != 0):
            print 'backup oclint.xml error! Stop!'
            return
        tree = ET.ElementTree(file='oclint.xml.origin')
        root = tree.getroot()
        delItems = []
        for child in root:
            for one in child:
                if one.attrib['ruleset'] == 'clang':
                    print child.attrib['name']
                    delItems.append(child)
                    break
                    #root.remove(child)

        for delItem in delItems:
            root.remove(delItem)

        tree.write('oclint.xml')

class Sonar():
    def __init__(self, jsonData, project):
        self.projectKey = jsonData['projectKey']
        self.host = jsonData['host']
        self.login = jsonData['login']
        self.password = jsonData['password']
        self.project = project
        self.runResult = False

    def genProperties(self):
        fp = open('sonar-project.properties', 'w')
        fp.write('sonar.projectKey=%s\n' % self.projectKey)
        fp.write('sonar.host.url=%s\n' % self.host)
        fp.write('sonar.login=%s\n' % self.login)
        fp.write('sonar.password=%s\n' % self.password)
        fp.write('\n')

        fp.write('sonar.language=objc\n')
        fp.write('sonar.objectivec.workspace=%s\n' % self.project.workspace)
        fp.write('sonar.objectivec.appScheme=%s\n' % self.project.scheme)
        fp.write('sonar.sources=%s\n' % self.project.src)
        fp.write('\n')

        fp.write('sonar.objectivec.oclint.report=oclint.xml\n')
        fp.close()

    def runScanner(self):
        self.runResult = runCmd('sonar-scanner')

    def isSuccess(self):
        return self.runResult == 0

def exitWithCode(code):
    if not isTest:
        sys.exit(code)

def checkParam(params):
    global isTest, useGit
    for p in params:
        if p == '-test':
            isTest = True
        elif p == '-git':
            useGit = True

def main():
    # 加载配置文件
    jsonData = None
    if len(sys.argv) >= 2:
        print '\033[91m---> Load config file ...\033[0m'
        config = open(sys.argv[1])
        jsonData = json.load(config)
        config.close()
        checkParam(sys.argv)
    else:
        print 'Usage: sonar.py project.json'
        print '       sonar.py project.json -test -git'
        sys.exit(1)

    #------------------------------------------------
    # 0. 清理工程、日志
    #------------------------------------------------
    if useGit:
        os.system('rm -fr ' + workpath)

    #------------------------------------------------
    # 1.项目编译
    #------------------------------------------------
    project = Project(jsonData['project'])

    if useGit and not isTest:
        # 处理源代码
        project.clone()
        # 切换到源代码目录
        os.chdir(os.path.join(os.getcwd(), workpath))
        # 切换分支
        project.checkout()

    # 清理文件
    if not useGit:
        os.system('rm oclint.xml oclint.xml.origin .oclint xcodebuild.log sonar-project.properties compile_commands.json')

    # 清理上一次编译
    print '---> Clean build ...'
    project.clean()

    # 编译项目，生成compile_commands.json
    print '---> Build project...'
    project.build()

    if not project.isSuccess():
        print 'Build Error: check buildlog or compile_commands.json'
        print 'STOP!!!'
        exitWithCode(1)

    #------------------------------------------------
    # 2.OClint生成分析报告oclint.xml
    #------------------------------------------------
    print '---> Run oclint...'
    oclint = OClint(jsonData['oclint'])
    oclint.run()

    # 删掉oclint.xml中的compile warning
    oclint.rmClangRules()

    if not oclint.isSuccess():
        print 'OcLint Error: check oclint.xml and oclint.xml.origin'
        print 'STOP!!!'
        exitWithCode(1)

    #------------------------------------------------
    # 3.执行sonar-scanner上传分析报告
    #------------------------------------------------
    print '---> Run sonar-scanner...'
    sonar = Sonar(jsonData['sonar'], project)
    sonar.genProperties()
    sonar.runScanner()

    if not sonar.isSuccess():
        print 'SonarScanner Error: check build.log'
        print 'STOP!!!'
        exitWithCode(1)

    print "Success!"

if __name__ == '__main__':
    main()
