<template lang="pug">
v-menu(v-model="active")
  template(#activator="{ on, attrs }")
    slot(name="default" :on="on" :attrs="attrs")
  v-list
    v-list-item Заполнить форму
    v-list-item Выбрать из файла
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { PeriodType } from '~/types/graphql'

export default defineComponent({
  props: {
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup () {
    const active = ref<boolean>(false)
    return { active }
  }
})
</script>
