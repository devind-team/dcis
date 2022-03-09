<template lang="pug">
  v-tooltip(bottom)
    template(v-slot:activator="{ on }")
      v-btn(v-on="on" icon)
        v-icon mdi-lock-reset
    span {{ $t('ac.users.components.resetPasswords.resetPassword') }}
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
