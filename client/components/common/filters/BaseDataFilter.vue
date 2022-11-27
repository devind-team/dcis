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
  template(#activator="{ on, attrs }")
    slot(
      name="message"
      :on="on"
      :attrs="attrs"
      :message="message"
      :container-class="messageContainerClass"
    )
      v-chip(
        v-on="on"
        v-bind="attrs"
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
import type { PropType } from '#app'
import { defineComponent, ref, watch } from '#app'
import { Class } from '~/types/filters'

export default defineComponent({
  components: { VMenu, VDialog },
  props: {
    title: { type: String, default: null },
    message: { type: String, required: true },
    messageContainerClass: { type: [String, Array, Object] as PropType<Class>, default: undefined },
    messageContainerClose: { type: Boolean, default: false },
    modal: { type: Boolean, default: false },
    fullscreen: { type: Boolean, default: undefined },
    maxWidth: { type: [String, Number], default: '400px' },
    maxHeight: { type: [String, Number], default: '400px' }
  },
  setup (_, { emit }) {
    const active = ref<boolean>(false)

    watch(() => active.value, (newValue) => {
      emit('active-changed', newValue)
    })

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
