<template>
    <div class="dep1-container">
      <Chat src='呼吸外科' />
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  import Chat from '@/views/component/Chat.vue';  // Corrected path
  
  export default {
    name: 'dep1',
    components: {
      Chat
    },
    computed: {
      ...mapGetters([
        'name'
      ])
    }
  }
  </script>
  
  <style lang="scss" scoped>
  .dep1 {
    &-container {
      overflow-y:hidden;
    }
    &-text {
      font-size: 30px;
      line-height: 46px;
    }
  }
  </style>
  