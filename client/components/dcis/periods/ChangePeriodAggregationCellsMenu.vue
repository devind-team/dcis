<template lang="pug">
v-menu(v-model="active", transition="slide-y-transition" offset-y left)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  v-list(dense)
    add-period-aggregation-cell(:period="period" :update="addUpdate")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-icon
            v-icon mdi-form-select
          v-list-item-content {{ $t('dcis.periods.aggregationCells.changeMenu.addAggregation.buttonText') }}
    update-period-aggregation-cells-from-file(:period="period", :update="fromFileUpdate")
      template(#activator="{ on, attrs }")
        v-list-item(v-on="on" v-bind="attrs")
          v-list-item-icon
            v-icon mdi-file-import-outline
          v-list-item-content {{ $t('dcis.periods.aggregationCells.changeMenu.updateAggregationFromFile.buttonText') }}
    v-list-item(
      loading="loading"
      @click="unloadAggregationsInFile"
    )
      v-list-item-icon
        v-icon mdi-file-export-outline
      v-list-item-content {{ $t('dcis.periods.aggregationCells.changeMenu.unloadAggregation.content') }}
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { AddUpdateType, ResetUpdateType } from '~/composables'
import {
  PeriodType,
  UnloadAggregationsInFileMutation,
  UnloadAggregationsInFileMutationVariables
} from '~/types/graphql'
import UpdatePeriodAggregationCellsFromFile from '~/components/dcis/periods/UpdatePeriodAggregationCellsFromFile.vue'
import AddPeriodAggregationCell from '~/components/dcis/periods/AddPeriodAggregationCell.vue'
import unloadAggregationsInFileMutation from '~/gql/dcis/mutations/aggregation/unload_aggregations_in_file.graphql'

export type UnloadAggregationsInFileMutationResult = { data: UnloadAggregationsInFileMutation }

export default defineComponent({
  components: { AddPeriodAggregationCell, UpdatePeriodAggregationCellsFromFile },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    fromFileUpdate: { type: Function as PropType<ResetUpdateType>, required: true },
    addUpdate: { type: Function as PropType<AddUpdateType>, required: true }
  },
  setup (props) {
    const active = ref<boolean>(false)

    const { mutate, loading, onDone } = useMutation<
      UnloadAggregationsInFileMutation,
      UnloadAggregationsInFileMutationVariables
    >(unloadAggregationsInFileMutation)
    onDone(({ data: { unloadAggregationsInFile: { success, src } } }: UnloadAggregationsInFileMutationResult) => {
      if (success) {
        close()
        const a = document.createElement('a')
        a.href = `/${src}`
        a.download = 'aggregations.json'
        a.click()
      }
    })

    const unloadAggregationsInFile = () => {
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
      unloadAggregationsInFile,
      close
    }
  }
})
</script>
