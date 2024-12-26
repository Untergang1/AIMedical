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
                    </el-radio-group>
                  </el-form-item>
              </el-row>
              <el-col>
                <el-button type="primary" :loading="loading" class="savebutton" @click="savePinfo"> 保存 </el-button>
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
              <el-form-item label="身高" prop="phone">
                <el-input v-model="resume.height" autocomplete="off"/>
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
              <el-form-item label="体重" prop="major">
                <el-input v-model="resume.weight" autocomplete="off"
                
                />
              </el-form-item>
            </el-col>
          </el-row>
        
          <el-row>
            <el-col :span="12">
              <el-form-item label="备注" prop="major">
                <el-input v-model="resume.ad" 
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
      console.log(this.$store.state.user.weight)
      return {
        resume: {
          sex: this.$store.state.user.sex, // 从 Vuex 中获取用户性别
          name: this.$store.state.user.name, // 从 Vuex 中获取用户名称
          age: this.$store.state.user.age , // 从 Vuex 中获取用户年龄
          height: this.$store.state.user.height, // 从 Vuex 中获取用户身高
          weight: this.$store.state.user.weight, // 从 Vuex 中获取用户体重
          ad: this.$store.state.user.addition, // 从 Vuex 中获取用户体重
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
          height: this.resume.height,
          age: this.resume.age,
          sex: this.resume.sex,
          weight: this.resume.weight,
          addition: this.resume.ad
        }).then((res => {
              if (res.code === 20000) {
                this.loading = false
                Message.success('保存成功')
              } else {
                this.loading = false
                Message.error('保存失败')
              }

              this.$store.dispatch('user/getInfo').then(()=> {
              this.resume.sex =  this.$store.state.user.sex
              this.resume.name =  this.$store.state.user.name
              this.resume.age =  this.$store.state.user.age
              this.resume.height =  this.$store.state.user.height
              this.resume.weight =  this.$store.state.user.weight
              this.resume.ad =  this.$store.state.user.addition
              })

            
              console.log(this.resume.height)

              //修改data
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
    margin-bottom: 5px;
  }
  /* In your component's <style scoped> section */
  
  </style>