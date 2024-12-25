const getters = {
  // Existing getters
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  sex: state => state.user.sex,

  // New getters based on the additional terms in getDefaultState
  realname: state => state.user.realname,
  age: state => state.user.age,
  height: state => state.user.height,
  weight: state => state.user.weight,
  isAuthenticated: state => !!state.user.token,  // Based on the token
};

export default getters
