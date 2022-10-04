<template lang="pug">
v-menu(v-model="active")
  template(#activator="{ on, attrs }")
    slot(name="default" :on="on" :attrs="attrs")
  v-list
    add-attribute(@close="close" :period="period" :update="update")
      template(#activator="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-form-select
          v-list-item-content Заполнить форму
    // v-list-item
    //  v-list-item-icon
    //    v-icon mdi-file
    //  v-list-item-content Выбрать из файла
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { defineComponent, PropType, ref } from '#app'
import { TranslateResult } from 'vue-i18n'
import { AttributeKind, PeriodType } from '~/types/graphql'
import AddAttribute, { AddAttributeMutationResult } from '~/components/dcis/attributes/AddAttribute.vue'

export const getAttributeKinds = t => ([
  'TEXT',
  'BIGMONEY',
  'BOOL',
  'DATE',
  'FILES',
  'MONEY',
  'NUMERIC'
].map<{text: TranslateResult, value: AttributeKind}>((tp: AttributeKind) => ({
  text: t(`dcis.attributes.addMenu.${tp.toLowerCase()}`),
  value: tp
})))

export default defineComponent({
  components: { AddAttribute },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: {
      type: Function as PropType<(cache: DataProxy, result: AddAttributeMutationResult) => void>,
      required: true
    }
  },
  setup (_, { emit }) {
    const active = ref<boolean>(false)

    const close = () => {
      active.value = false
      emit('close')
    }
    return { active, close }
  }
})
</script>
