<template lang="pug">
component(
  v-model="active"
  :is="modal ? 'v-dialog' : 'v-menu'"
  :max-width="maxWidth"
  :close-on-content-click="false"
  :fullscreen="fullscreen"
  bottom
  scrollable
)
  template(#activator="{ on }")
    slot(
      name="message"
      :on="on"
      :message="message"
      :container-class="messageContainerClass"
    )
      v-chip(
        v-on="on"
        :class="messageContainerClass"
        :close="messageContainerClose"
        @click:close="$emit('clear')"
      ) {{ message }}
  v-card.d-flex.flex-column(:max-height="maxHeight")
    v-card-title
      slot(name="title" :title="title")
        span {{ title }}
        template(v-if="modal")
          v-spacer
          v-btn(@click="close" icon)
            v-icon mdi-close
    v-card-subtitle
      slot(name="subtitle")
    slot(name="fixed-content")
    v-card-text.flex-grow-1.overflow-auto
      slot(name="item-content")
    v-card-actions
      slot(name="actions")
        v-btn.mr-2(color="warning" @click="reset") {{ $t('common.filters.baseDataFilter.reset') }}
        v-spacer
        v-btn.ml-2(color="primary" @click="apply") {{ $t('common.filters.baseDataFilter.apply') }}
</template>

<script lang="ts">
import { VMenu, VDialog } from 'vuetify/lib'
import type { PropType, Ref, SetupContext } from '#app'
import { defineComponent, ref } from '#app'
import { Class } from '~/types/filters'

export default defineComponent({
  components: { VMenu, VDialog },
  props: {
    message: { type: String, required: true },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: undefined },
    messageContainerClose: { type: Boolean, default: false },
    modal: { type: Boolean, default: false },
    fullscreen: { type: Boolean, default: undefined },
    title: {
      type: String,
      default () {
        return (this as any).$options.methods.t.call(this, 'title')
      }
    },
    maxWidth: { type: [String, Number], default: '400px' },
    maxHeight: { type: [String, Number], default: '400px' }
  },
  setup (_, { emit }: SetupContext) {
    const active: Ref<boolean> = ref<boolean>(false)

    const close = () => {
      active.value = false
      emit('close')
    }

    const reset = () => {
      active.value = false
      emit('reset')
    }

    const apply = () => {
      active.value = false
      emit('apply')
    }

    return { active, close, reset, apply }
  }
})
</script>
