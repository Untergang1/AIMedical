<template>
    <div class="pinfo-interface">
      <el-card>
        <el-row style="margin-bottom: 0px; width: 200px;">
          <p style="margin-left: 15px">个人信息设置</p>
        </el-row>
        <el-form ref="form"  >
        
          <el-row>
            <el-col :span="7">
              <el-row>
                <el-form-item label="性别" prop="sex">
                    <el-radio-group v-model="resume.sex">
                      <el-radio label="男">男</el-radio>
                      <el-radio label="女">女</el-radio>
                      <el-radio label="保密">保密</el-radio>
                    </el-radio-group>
                  </el-form-item>
              </el-row>
              <el-col>
                <el-button type="primary" :loading="loading" icon="el-icon-edit" class="savebutton" @click="savePinfo"></el-button>
              </el-col>
            </el-col>
            <el-col :span="5">
                <img :src="avatar" class="useravatar">
              </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <el-form-item label="姓名" prop="name">
                <el-input 
                :disabled="true"
                v-model="resume.name" 
                autocomplete="off"/>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <el-form-item label="电话" prop="phone">
                <el-input v-model="resume.phone" autocomplete="off"/>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <el-form-item label="年龄" prop="age">
                <el-input v-model="resume.age" autocomplete="off"/>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <el-form-item label="住址" prop="major">
                <el-input v-model="resume.loc" autocomplete="off"
                
                />
              </el-form-item>
            </el-col>
          </el-row>
        
          <el-row>
            <el-col :span="12">
              <el-form-item label="备注" prop="major">
                <el-input v-model="resume.addition" 
                          autocomplete="off"
                          type="textarea"
                          rows="10"
                          size="medium" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  import { saveInfo } from '@/api/user';
  import { Message } from 'element-ui'

  export default {
    name: 'pinfo',
    data() {
      return {
        resume: {
          sex: '',
          name: this.$store.state.user.realname,
          phone: '',
          age: '',
          loc: '',
          addition: '',
          // 其他字段根据实际需要继续补充
        },
        rules: {
          // 校验规则可以根据实际情况进行定义
        },
        loading: false
      }
    },
    methods: {
      savePinfo() {
        this.loading = true
        saveInfo({
          name: this.resume.name,
          phone: this.resume.phone,
          age: this.resume.age,
          sex: this.resume.sex,
          loc: this.resume.loc,
          addition: this.resume.addition
        }).then((res => {
              if (res.code === 20000) {
                this.loading = false
                Message.success('保存成功')
                this.toggleForm()
              } else {
                this.loading = false
                Message.error('保存失败')
              }
            }))
      }
      // 其他方法根据实际需要继续补充
    },
    computed: {
    ...mapGetters([
      'avatar',
      'realname'
    ])
    }
    
  }
  </script>
  


  <style scoped>
  .pinfo-interface {
    overflow: hidden;
  }

  .el-card {
    margin: 10px 25px;
    height: 750px;
  }
  
  .el-form-item {
    margin-bottom: 20px;
  }
  
  .el-button {
    margin-right: 10px;
  }
  
  .el-input {
    width: 80%;
  }
  .useravatar {
    margin-bottom: 10%;
    width: 100px;
    height: 100px;
  }
  .savebutton {
    width: 100px;
  }
  /* In your component's <style scoped> section */
  
  </style>