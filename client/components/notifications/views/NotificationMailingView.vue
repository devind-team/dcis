<template lang="pug">
  v-card
    v-card-title {{ mailing.header }}
    v-card-subtitle {{ $filters.dateTimeHM(mailing.createdAt) }}
    v-card-text(v-html="mailing.text")
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import { Component, Prop } from 'vue-property-decorator'
import { MailingType } from '~/types/graphql'

@Component<NotificationMailingView>({})
export default class NotificationMailingView extends Vue {
  @Prop({ type: Object as PropType<MailingType>, required: true }) mailing!: MailingType
}
</script>
