<template lang="pug">
v-navigation-drawer(
  :value="active"
  :permanent="$vuetify.breakpoint.mdAndUp"
  :temporary="$vuetify.breakpoint.smAndDown"
  :clipped="$vuetify.breakpoint.mdAndUp"
  :mini-variant="$vuetify.breakpoint.mdAndUp"
  :expand-on-hover="$vuetify.breakpoint.mdAndUp"
  fixed
  app
  @input="$emit('change', $event)"
)
  v-list
    template(v-for="item in items")
      v-list-item(
        v-if="item.permissions === undefined || item.permissions && hasPerm(item.permissions)"
        :to="localePath({ name: item.to, params: item.params, query: item.query })"
        link
      )
        v-list-item-icon
          v-icon mdi-{{ item.icon }}
        v-list-item-content
          v-list-item-title {{ item.title }}
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { LinksType } from '~/types/devind'
import { useAuthStore } from '~/stores'

export default defineComponent({
  model: { prop: 'active', event: 'change' },
  props: {
    items: { type: Array as PropType<LinksType[]>, required: true },
    active: { type: Boolean, required: true }
  },
  setup () {
    const { hasPerm } = useAuthStore()
    return { hasPerm }
  }
})
</script>
