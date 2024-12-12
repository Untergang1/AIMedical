<template>
    <div class="dep3-container">
      <Chat src="耳鼻喉科"/>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex'
  import Chat from '@/views/component/Chat.vue';  // Corrected path
  
  export default {
    name: 'dep3',
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
  .dep3 {
    &-container {
      overflow-y:hidden;
    }
    &-text {
      font-size: 30px;
      line-height: 46px;
    }
  }
  </style>
  