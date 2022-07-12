<template lang="pug">
v-tooltip(bottom)
  template(v-slot:activator="{ on }")
    v-btn(v-on="on" icon)
      v-icon mdi-bell-ring
  span {{ $t('ac.users.components.sendNotification.sendNotification') }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { UserType } from '~/types/graphql'

export default defineComponent({
  props: {
    user: { type: Object as PropType<UserType>, required: true }
  }
})
</script>
