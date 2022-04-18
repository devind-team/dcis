<template lang="pug">
  v-container
    v-row
      v-col(v-if="error.statusCode === 403 " style="height: 76vh")
        error403
      v-col(v-else-if ="error.statusCode === 404 " style="height: 76vh")
        error404
      v-col(v-else-if ="error.statusCode === 500 " style="height: 76vh")
        error500
      v-col(v-else style="height: 76vh")
        pre {{ error }}
      v-container
        v-col.text-right
          v-btn.mr-n15.mt-n8(:to="localePath({ name: 'index' })" color="primary" x-large) {{ $t('error.home') }}
</template>

<script lang="ts">
import { defineComponent, useNuxt2Meta } from '#app'
import Error403 from '~/components/errors/Error403.vue'
import Error404 from '~/components/errors/Error404.vue'
import Error500 from '~/components/errors/Error500.vue'

export default defineComponent({
  components: { Error403, Error404, Error500 },
  props: {
    error: { type: Object, required: true }
  },
  setup () {
    useNuxt2Meta({ title: 'Что-то пошло не так' })
  }
})
</script>
