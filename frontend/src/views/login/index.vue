<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">

      <div class="title-container">
        <h3 class="title">欢迎来到智能问诊平台</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          name="username"
          type="text"
          placeholder="请输入用户名"
          tabindex="1"
          auto-complete=""
        />
      </el-form-item>

      <el-form-item v-if="isLoginForm" prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="请输入密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLoginOrRegister"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>


      <el-form-item v-if="!isLoginForm" prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="请输入密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native=""
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>

      <el-form-item v-if="!isLoginForm" prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          v-model="loginForm.repassword"
          :type="passwordType"
          placeholder="请再次输入密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLoginOrRegister"
        />
      </el-form-item>



      <!-- 登录/注册按钮 -->
      <el-button
        :loading="loading"
        type="primary"
        style="width:100%;margin-bottom:30px;"
        @click.native.prevent="handleLoginOrRegister"
      >{{ activeButton }}
      </el-button>

      <!-- 切换按钮 -->

      <div class="mb-4">
        <el-button   @click="toggleForm">
          {{ isLoginForm ? '注册新账号' : '返回登录' }}
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script>
import { register } from '@/api/user';
import { validUsername } from '@/utils/validate'
import { Message } from 'element-ui'


export default {
  name: 'Login',
  data() {
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能少于六位'))
      } else {
        callback()
      }
    }
    const validateId = (rule, value, callback) => {
      if (value.length != 18) {
        callback(new Error('身份证位数错误'))
      } else {
        callback()
      }
    }

    return {
      loginForm: {
        username: 'admin',
        password: '',
        repassword: '',
        name: '',
        id: ''
      },
      loginRules: {
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        // id: [{ required: true, trigger: 'blur', validator: validateId }],
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      isLoginForm: true,
      activeButton:"登 陆",
      pname: '',
      id: '',
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    clearAll(){
      this.loginForm.password = ''
      this.loginForm.username = ''
      this.loginForm.repassword = ''
      this.name = ''
      this.id = ''
    }
    ,
    handleLoginOrRegister() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          if(this.isLoginForm){
            this.$store.dispatch('user/login', this.loginForm).then(() => {
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
            }).catch(() => {
              this.loading = false
            })
          } else {
            //handling the register
            console.log('registering')
            register(this.loginForm).then((res => {
              if (res.code === 20000) {
                this.loading = false
                Message.success('注册成功')
                this.toggleForm()
              } else {
                this.loading = false
                Message.error(res.message)
              }
            }))
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
    ,
    toggleForm() {
      this.isLoginForm = !this.isLoginForm
      this.activeButton = this.isLoginForm ? '登 录' : '注 册'
      this.clearAll()
      this.$nextTick(() => {
        this.$refs.username.focus()
      })
    }


  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {

  

  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;
  background-image: url("~@/assets/login-bg.svg");
  background-size: 100%;
  display: flex;
  align-items: center;

  .login-form {
    position: relative;
    width: 520px;

    max-width: 100%;

    margin: 0 auto;
  
    border-radius: 8px;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
