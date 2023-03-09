<template lang="pug">
v-menu(v-model="active")
  template(#activator="{ on, attrs }")
    slot(name="default" :on="on" :attrs="attrs")
  v-list
    add-attribute(@close="close" :period="period" :update="addUpdate")
      template(#activator="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-form-select
          v-list-item-content Заполнить форму
    v-list-item(
      loading="loading"
      @click="unloadAttributesInFile"
    )
      v-list-item-icon
        v-icon mdi-file
      v-list-item-content {{ $t('dcis.attributes.unloadAttributes.content') }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { defineComponent, PropType, ref } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { TranslateResult } from 'vue-i18n'
import { ResetUpdateType } from '~/composables'
import {
  AttributeKind,
  PeriodType,
  UnloadAttributesInFileMutation,
  UnloadAttributesInFileMutationVariables
} from '~/types/graphql'
import unloadAttributesInFileMutation from '~/gql/dcis/mutations/attributes/unload_attributes_in_file.graphql'
import AddAttribute, { AddAttributeMutationResult } from '~/components/dcis/attributes/AddAttribute.vue'
export type UnloadAttributesInFileMutationResult = { data: UnloadAttributesInFileMutation }

export const getAttributeKinds = t => ([
  'TEXT',
  'NUMERIC',
  'BIGMONEY',
  'BOOL',
  'DATE',
  'FILES',
  'MONEY'
].map<{text: TranslateResult, value: AttributeKind}>((tp: AttributeKind) => ({
  text: t(`dcis.attributes.addMenu.${tp.toLowerCase()}`),
  value: tp
})))

export default defineComponent({
  components: { AddAttribute },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    addUpdate: {
      type: Function as PropType<(cache: DataProxy, result: AddAttributeMutationResult) => void>,
      required: true
    },
    fromFileUpdate: { type: Function as PropType<ResetUpdateType>, required: true }
  },
  setup (props, { emit }) {
    const active = ref<boolean>(false)

    const { mutate, loading, onDone } = useMutation<
      UnloadAttributesInFileMutation,
      UnloadAttributesInFileMutationVariables
    >(unloadAttributesInFileMutation)
    onDone(({ data: { unloadAttributesInFile: { success, src } } }: UnloadAttributesInFileMutationResult) => {
      if (success) {
        close()
        const a = document.createElement('a')
        a.href = `/${src}`
        a.download = 'attrebutes.json'
        a.click()
      }
    })

    const unloadAttributesInFile = () => {
      mutate({
        periodId: props.period.id
      })
    }

    const close = () => {
      active.value = false
      emit('close')
    }
    return {
      active,
      loading,
      unloadAttributesInFile,
      close
    }
  }
})
</script>
