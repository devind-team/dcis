<template lang="pug">
div(ref="container")
  div(ref="content" :class="contentClasses")
    slot
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch, nextTick } from '#app'
import { useVuetify } from '~/composables'

export default defineComponent({
  props: {
    isFullScreen: { type: Boolean, required: true }
  },
  setup (props) {
    const container = ref<HTMLDivElement | null>(null)
    const content = ref<HTMLDivElement | null>(null)

    const { isDark } = useVuetify()

    const contentClasses = computed<Record<string, boolean>>(() => ({
      'full-screen-in-place__content': props.isFullScreen,
      'full-screen-in-place__content_light': props.isFullScreen && !isDark.value,
      'full-screen-in-place__content_dark': props.isFullScreen && isDark.value
    }))

    watch(() => props.isFullScreen, async (newValue) => {
      await nextTick()
      if (newValue) {
        document.querySelector('#app').append(content.value)
        document.documentElement.classList.add('overflow-y-hidden')
      } else {
        container.value.append(content.value)
        document.documentElement.classList.remove('overflow-y-hidden')
      }
    })

    return { container, content, contentClasses }
  }
})
</script>

<style lang="sass">
.full-screen-in-place__content
  position: fixed
  left: 0
  top: 0
  width: 100vw
  height: 100vw
  z-index: 5
  padding-left: 10px
.full-screen-in-place__content_light
  background: white
.full-screen-in-place__content_dark
  background: #1E1E1E
</style>
