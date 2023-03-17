<template lang="pug">
v-menu(v-model="active" transition="slide-y-transition" offset-y left)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  v-list(dense)
    add-period-limitation(v-if="period.canChangeLimitations" :period="period" :update="addUpdate")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-icon
            v-icon mdi-form-select
          v-list-item-content {{ $t('dcis.periods.limitations.changeMenu.addLimitation.buttonText') }}
    update-period-limitations-from-file(v-if="period.canChangeLimitations" :period="period" :update="fromFileUpdate")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-icon
            v-icon mdi-file-import-outline
          v-list-item-content {{ $t('dcis.periods.limitations.changeMenu.updateLimitationFromFile.buttonText') }}
    v-list-item(
      loading="loading"
      @click="unloadLimitationsInFile"
    )
      v-list-item-icon
        v-icon mdi-file-export-outline
      v-list-item-content {{ $t('dcis.periods.limitations.changeMenu.unloadLimitation.content') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { AddUpdateType, ResetUpdateType } from '~/composables'
import {
  PeriodType,
  UnloadLimitationsInFileMutation,
  UnloadLimitationsInFileMutationVariables
} from '~/types/graphql'
import AddPeriodLimitation from '~/components/dcis/periods/AddPeriodLimitation.vue'
import UpdatePeriodLimitationsFromFile from '~/components/dcis/periods/UpdatePeriodLimitationsFromFile.vue'
import unloadLimitationsInFileMutation from '~/gql/dcis/mutations/limitation/unload_limitations_in_file.graphql'

export type UnloadLimitationsInFileMutationResult = { data: UnloadLimitationsInFileMutation }

export default defineComponent({
  components: { UpdatePeriodLimitationsFromFile, AddPeriodLimitation },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    fromFileUpdate: { type: Function as PropType<ResetUpdateType>, required: true },
    addUpdate: { type: Function as PropType<AddUpdateType>, required: true }
  },
  setup (props) {
    const active = ref<boolean>(false)

    const { mutate, loading, onDone } = useMutation<
      UnloadLimitationsInFileMutation,
      UnloadLimitationsInFileMutationVariables
    >(unloadLimitationsInFileMutation)
    onDone(({ data: { unloadLimitationsInFile: { success, src } } }: UnloadLimitationsInFileMutationResult) => {
      if (success) {
        close()
        const a = document.createElement('a')
        a.href = `/${src}`
        a.download = 'limitations.json'
        a.click()
      }
    })

    const unloadLimitationsInFile = () => {
      mutate({
        periodId: props.period.id
      })
    }

    const close = () => {
      active.value = false
    }

    return {
      active,
      loading,
      unloadLimitationsInFile,
      close
    }
  }
})
</script>
