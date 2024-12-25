import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: '',
    realname: 'Joe Biden',
    age: '',
    height: '',
    weight: '',
    sex: '',
    addition: ''
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_RNAME: (state, rname) => {
    state.realname = rname
  },
  SET_AGE: (state, age) => {
    state.age = age
  },
  SET_HEIGHT: (state, height) => {
    state.height = height
  },
  SET_WEIGHT: (state, weight) => {
    state.weight = weight
  },
  SET_SEX: (state, sex) => {
    state.sex = sex
  },
  SET_AD: (state, ad) => {
    state.addition = ad
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        console.log(response)
        commit('SET_TOKEN', data.token)
        setToken(data.token)  

        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const { data } = response

        if (!data) {
          return reject('Verification failed, please Login again.')
        }

        const { username, avatar, age, sex, height, weight, addition } = data

        commit('SET_NAME', username)
        commit('SET_AVATAR', avatar)
        commit('SET_AGE', age)
        commit('SET_HEIGHT', height)
        commit('SET_WEIGHT', weight)
        commit('SET_SEX', sex)
        commit('SET_AD', addition)

        console.log(state.weight)

        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
