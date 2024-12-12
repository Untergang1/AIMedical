<template>
    <div class="dashboard-container">
   
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  import Chat from '@/views/component/Chat.vue';  // Corrected path
  
  export default {
    name: 'departments',
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
  .dashboard {
    &-container {
      overflow-y:hidden;
    }
    &-text {
      font-size: 30px;
      line-height: 46px;
    }
  }
  </style>
  