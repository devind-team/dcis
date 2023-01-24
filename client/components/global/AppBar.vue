<template lang="pug">
v-app-bar(app clipped-left)
  v-app-bar-nav-icon(v-show="$vuetify.breakpoint.smAndDown" @click="drawer = !drawer")
  slot(name="icon")
    v-img(:src="$getSettingValue('APP_ICON') || '/icon.png'" max-height="40" max-width="40")
  v-toolbar-title.ml-2
    slot(name="title")
      nuxt-link(:to="localePath({ name: 'index' })" style="text-decoration: none") {{ $getSettingValue('APP_NAME') }}
  v-spacer
  v-toolbar-items
    template(v-if="loginIn")
      notification(v-if="$vuetify.breakpoint.smAndUp")
      v-btn(v-else :to="localePath({ name: 'notifications' })" icon)
        v-icon mdi-bell
      avatar-menu
    template(v-else)
      slot(name="notAuthorized")
        v-btn(:to="localePath({ name: 'auth-login' })" text) {{ $t('auth.login.login') }}
</template>

<script lang="ts">
import { useVModel } from '@vueuse/core'
import type { Ref } from '#app'
import { defineComponent, toRef } from '#app'
import { useAuthStore } from '~/stores'
import Notification from '~/components/global/Notification.vue'
import AvatarMenu from '~/components/global/AvatarMenu.vue'

export default defineComponent({
  components: { Notification, AvatarMenu },
  props: {
    value: { type: Boolean, required: true }
  },
  setup (props, { emit }) {
    const authStore = useAuthStore()

    const loginIn: Readonly<Ref<boolean>> = toRef(authStore, 'loginIn')
    const drawer: Ref<boolean> = useVModel(props, 'value', emit)

    return { drawer, loginIn }
  }
})
</script>
