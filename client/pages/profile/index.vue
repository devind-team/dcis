<template lang="pug">
  v-progress-circular(color="primary" indeterminate)
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { Context } from '@nuxt/types'

@Component<ProfileIndexPage>({
  middleware: 'auth',
  async asyncData ({ redirect, app: { localePath } }: Context) {
    await redirect(localePath({ name: 'profile-me' }))
  }
})
export default class ProfileIndexPage extends Vue { }
</script>
