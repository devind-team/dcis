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
import Vue, { AsyncComponent } from 'vue'
import { Component, Prop } from 'vue-property-decorator'
import { MetaInfo } from 'vue-meta'
const Error403: AsyncComponent = () => import('~/components/errors/Error403.vue')
const Error404: AsyncComponent = () => import('~/components/errors/Error404.vue')
const Error500: AsyncComponent = () => import('~/components/errors/Error500.vue')

@Component<ErrorLayout>({
  components: { Error403, Error404, Error500 },
  head (): MetaInfo {
    return { title: 'Что-то пошло не так' } as MetaInfo
  }
})
export default class ErrorLayout extends Vue {
  @Prop({ default: null }) error: any
}
</script>
