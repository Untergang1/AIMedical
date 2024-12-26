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
    username: data.name,
    height: data.height,
    age: data.age,
    sex: data.sex,
    weight: data.weight,
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
  }
  return request({
    url: '/user/register',
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
    url: '/user/logout',
    method: 'post'
  })
}
