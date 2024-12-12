<template>
  <div class="pinfo-container">
    <pinfo />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import pinfo from '@/views/component/pinfo.vue';  // Corrected path

export default {
  name: 'information',
  components: {
    pinfo
  },
  computed: {
    ...mapGetters([
    ])
  }
}
</script>

<style lang="scss" scoped>
.pinfo {
  &-container {
    overflow-y:hidden;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
