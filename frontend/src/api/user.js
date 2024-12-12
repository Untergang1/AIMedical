import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'user/login',
    method: 'post',
    data
  })
}

export function saveInfo(data){
  const sendData = {
    name: data.name,
    phone: data.phone,
    age: data.age,
    sex: data.sex,
    loc: data.loc,
    addition: data.addition
  }
  return request({
    url: '/user/info',
    method: 'post',
    headers: {
      'Content-Type': 'application/json' // Set the Content-Type to application/json
    },
    data: JSON.stringify(sendData) 
  })
}

export function sendChat(data){
  return request({
    url: '/user/chat',
    method: 'post',
    headers: {
      'Content-Type': 'application/json' // Set the Content-Type to application/json
    },
    data: JSON.stringify(data) 
  })
}

export function register(data) {
  const sendData = {
    username: data.username,
    password: data.password,
    name: data.name,
    id: data.id
  }
  return request({
    url: '/vue-admin-template/user/register',
    method: 'post',
    headers: {
      'Content-Type': 'application/json' // Set the Content-Type to application/json
    },
    data: JSON.stringify(sendData) 
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
