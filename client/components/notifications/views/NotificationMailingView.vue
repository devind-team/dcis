<template lang="pug">
  v-card
    v-card-title {{ mailing.header }}
    v-card-subtitle {{ dateTimeHM(mailing.createdAt) }}
    v-card-text(v-html="mailing.text")
</template>

<script lang="ts">
import type { PropType } from '#app'
import { defineComponent } from '#app'
import { useFilters } from '~/composables'
import { MailingType } from '~/types/graphql'

export default defineComponent({
  props: {
    mailing: { type: Object as PropType<MailingType>, required: true }
  },
  setup () {
    const { dateTimeHM } = useFilters()
    return { dateTimeHM }
  }
})
</script>
