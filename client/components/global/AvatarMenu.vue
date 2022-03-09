<template lang="pug">
  v-menu(left bottom)
    template(#activator="{ on }")
      v-btn(v-on="on" icon)
        v-avatar(v-on="on" color="primary")
          v-img(v-if="!!user.avatar" :src="`/${user.avatar}`")
          .headline(v-else) {{ user.lastName[0] }}{{ user.firstName[0] }}
    v-list
      template(v-for="item in items")
        v-list-item(v-if="!!item.permissions ? hasPerm(item.permissions) : true" :key="item.name" :to="localePath({ name: item.path })")
          v-list-item-icon
            v-icon mdi-{{ item.icon }}
          v-list-item-content
            v-list-item-title {{ $t(`avatarMenu.${item.name}`) }}
</template>

<script lang="ts">
import { defineComponent, toRefs } from '#app'
import { HasPermissionFnType, useAuthStore } from '~/store'
import { UserType } from '~/types/graphql'

export type AvatarMenuItem = {
  name: string,
  icon: string,
  path: string,
  permissions?: string | string[]
}

export default defineComponent({
  setup () {
    const authStore = useAuthStore()
    const { user, hasPerm } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(authStore)
    const items: AvatarMenuItem[] = [
      { name: 'profile', icon: 'face-man', path: 'profile-me' },
      { name: 'dcis', icon: 'table-network', path: 'dcis' },
      { name: 'controlPanel', icon: 'cog', path: 'panel', permissions: 'core.view_user' },
      { name: 'infoPanel', icon: 'view-dashboard-outline', path: 'dashboard', permissions: 'core.view_user' },
      { name: 'logout', icon: 'logout', path: 'auth-logout' }
    ]
    return { user, hasPerm, items }
  }
})
</script>
