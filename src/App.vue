<template>
  <div id="app">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>项目配置</span>
      </div>
      <el-form ref="form" :model="project" label-width="80px" size="mini">
        <el-form-item label="Git仓库">
          <el-input v-model="project.git"></el-input>
        </el-form-item>
        <el-form-item label="Git分支">
          <el-input v-model="project.branch"></el-input>
        </el-form-item>
        <el-form-item label="Workspace">
          <el-input v-model="project.workspace"></el-input>
        </el-form-item>
        <el-form-item label="Project">
          <el-input v-model="project.project"></el-input>
        </el-form-item>
        <el-form-item label="Scheme">
          <el-input v-model="project.scheme"></el-input>
        </el-form-item>
        <el-form-item label="SDK">
          <el-input v-model="project.sdk"></el-input>
        </el-form-item>
        <el-form-item label="代码目录">
          <el-input v-model="project.src"></el-input>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>Oclint配置</span>
      </div>
      <el-form ref="form" :model="project" label-width="100px" size="mini">
        <el-form-item label="过滤文件夹">
          <el-input v-model="oclint.exclude"></el-input>
        </el-form-item>
        <el-form-item label="行最大长度">
          <el-input v-model="oclint.longLine"></el-input>
        </el-form-item>
        <el-form-item label="函数最大行数">
          <el-input v-model="oclint.longMethod"></el-input>
        </el-form-item>
        <el-form-item label="圈复杂度">
          <el-input v-model="oclint.cyclomaticComplexity"></el-input>
        </el-form-item>
        <el-form-item label="变量最大长度">
          <el-input v-model="oclint.longVariableName"></el-input>
        </el-form-item>
        <el-form-item label="禁用规则">
          <el-checkbox-group v-model="oclint.disableRules">
            <el-checkbox label="UnusedMethodParameter" name="disableRules"></el-checkbox>
            <br>
            <el-checkbox label="AssignIvarOutsideAccessors" name="disableRules"></el-checkbox>
            <br>
            <el-checkbox label="ShortVariableName" name="disableRules"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="box-card">
      <div slot="header">
        <span>Sonar配置</span>
      </div>
      <el-form ref="form" :model="sonar" label-width="80px" size="mini">
        <el-form-item label="ProjectKey">
          <el-input v-model="sonar.projectKey"></el-input>
        </el-form-item>
        <el-form-item label="Host">
          <el-input v-model="sonar.host"></el-input>
        </el-form-item>
        <el-form-item label="Login">
          <el-input v-model="sonar.login"></el-input>
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="sonar.password"></el-input>
        </el-form-item>
      </el-form>
    </el-card>

    <el-button class="submit-btn" type="primary" @click="onSubmit">生成配置文件</el-button>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      project: {
        git: '',
        branch: '',
        workspace: '',
        project: '',
        scheme: '',
        sdk: 'iphonesimulator11.1',
        src: ''
      },
      oclint: {
        exclude: 'Pods',
        longLine: '1000',
        longMethod: '200',
        longVariableName: '40',
        cyclomaticComplexity:'10',
        disableRules: ['UnusedMethodParameter', 'AssignIvarOutsideAccessors', 'ShortVariableName']
      },
      sonar: {
        projectKey: '',
        host: 'http://localhost:9000',
        login: 'admin',
        password: 'admin'
      }
    }
  },
  methods: {
    onSubmit() {
      console.log('submit!');
      var project = this.project;
      var sonar = this.sonar;
      var oclint = this.oclint;
      if(this.checkItem(project.workspace, '请填写项目workspace')
        && this.checkItem(project.git, '请填写Git仓库')
        && this.checkItem(project.branch, '请填写Git分支')
        && this.checkItem(project.project, '请填写project')
        && this.checkItem(project.scheme, '请填写scheme')
        && this.checkItem(project.src, '请填写项目代码目录')
        && this.checkItem(sonar.projectKey, '填写ProjectKey')
        && this.checkItem(sonar.host, '请填写Sonar Host')
        && this.checkItem(sonar.login, '请填写Sonar Login')
        && this.checkItem(sonar.password, '请填写Sonar Password')) {
          this.saveToJson(sonar.projectKey + '.json', {project: project, oclint: oclint, sonar: sonar})
      }
    },
    checkItem(item, msg) {
      if (item.length < 1) {
        this.$message(msg);
        return false
      }
      return true;
    },
    saveToJson(filename, content) {
      console.log(filename + JSON.stringify(content, null, 2));
      var uriContent = "data:application/octet-stream," + encodeURIComponent(JSON.stringify(content, null, 2));
      var downloadLink = document.createElement("a");
      downloadLink.href = uriContent;
      downloadLink.download = filename;

      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    }
  }
}
</script>

<style>
  html, body {
    overflow-y: visible;
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    width: 500px;
    margin: 0 auto;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    margin-bottom: 20px;
    margin-top: 20px;
  }

  .submit-btn {
    margin-left: 160px;
  }

</style>
