<template>
  <div class="dashboard-container">
    <Chat src="导诊台"/>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Chat from '@/views/component/Chat.vue';  // Corrected path

export default {
  name: 'Dashboard',
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
