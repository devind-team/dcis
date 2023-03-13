<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.periods.aggregationCells.changeMenu.addAggregation.header'))"
  :subheader="period.name"
  :button-text="String($t('dcis.periods.aggregationCells.changeMenu.addAggregation.buttonText'))"
  :mutation="addAggregationMutation"
  :variables="variables"
  :update="(cache, result) => update(cache, result, 'aggregationCells', false)",
  mutation-name="addAggregation"
  i18n-path="dcis.periods.aggregationCells.changeMenu.addAggregation"
  @close="close"
)
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  template(#form)
    v-row
      v-col(cols="12" md="7")
        validation-provider(
          v-slot="{ errors, valid }"
          :name="String($t('dcis.periods.aggregationCells.changeMenu.addAggregation.sheet'))"
          rules="required"
        )
          v-select(
            v-model="sheetCell"
            :items="period.sheets"
            :label="$t('dcis.periods.aggregationCells.changeMenu.addAggregation.sheet')"
            :error-messages="errors"
            :success="valid"
            item-text="name"
            return-object
            autofocus
          )
      v-col(cols="12" md="5")
        validation-provider(
          v-slot="{ errors, valid }"
          :name="String($t('dcis.periods.aggregationCells.changeMenu.addAggregation.cell'))"
          rules="required"
        )
          v-text-field(
            v-model="aggregationCell"
            :label="$t('dcis.periods.aggregationCells.changeMenu.addAggregation.cell')"
            :error-messages="errors"
            :success="valid"
          )
    v-combobox(
      v-model="aggregationKind"
      :items="aggregationItems"
      :label="$t('dcis.periods.aggregationCells.changeMenu.addAggregation.method')"
    )
    v-row
      v-col(cols="12" md="7")
        validation-provider(
          v-slot="{ errors, valid }"
          :name="String($t('dcis.periods.aggregationCells.changeMenu.addAggregation.sheet'))"
          rules=""
        )
          v-select(
            v-model="sheetCells"
            :items="period.sheets"
            :label="$t('dcis.periods.aggregationCells.changeMenu.addAggregation.sheet')"
            :error-messages="errors"
            :success="valid"
            item-text="name"
            return-object
          )
      v-col(cols="12" md="5")
        validation-provider(
          v-slot="{ errors, valid }"
          :name="String($t('dcis.periods.aggregationCells.changeMenu.addAggregation.cell'))"
          rules=""
        )
          v-text-field(
            v-model="aggregationCells"
            :label="$t('dcis.periods.aggregationCells.changeMenu.addAggregation.cell')"
            :error-messages="errors"
            :success="valid"
          )
    v-row.justify-center
      v-btn(
        @click="addAggregationCellItem(sheetCells.name, aggregationCells)"
        color="primary"
      ) {{ $t('dcis.periods.aggregationCells.changeMenu.addCell.buttonText') }}
    v-list(v-if="aggregationCellItems")
      v-list-item(v-for="(item, index) in aggregationCellItems" :key="index")
        v-list-item-content
          v-list-item-title {{ item }}
        v-list-item-action
          v-btn(@click="deleteAggregationCellItem(index)" icon)
            v-icon(color="error") mdi-close
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { AddUpdateType, useI18n } from '~/composables'
import { AddAggregationMutationVariables, BaseSheetType, PeriodType } from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'
import addAggregationMutation from '~/gql/dcis/mutations/aggregation/add_aggregation.graphql'

const aggregationKinds = t => (['sum', 'avg', 'max', 'min'].map(value => ({
  text: t(`dcis.periods.aggregationCells.kinds.${value}`),
  value
})))

export default defineComponent({
  components: { MutationModalForm },
  props: {
    period: { type: Object as PropType<PeriodType>, required: true },
    update: { type: Function as PropType<AddUpdateType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()

    const aggregationItems = aggregationKinds(t)
    const aggregationKind = ref<{ text: string, value: string } | null>(null)

    const sheetCell = ref<BaseSheetType | null>(null)
    const aggregationCell = ref<string>('')

    const sheetCells = ref<BaseSheetType | null>(null)
    const aggregationCells = ref<string>('')

    const aggregationCellItems = ref<string[]>([])

    const transformation = (sheet: string, cell: string) => {
      return `'${sheet}'!${cell}`
    }

    const addAggregationCellItem = (sheet: string, cell: string) => {
      aggregationCellItems.value.push(transformation(sheet, cell))
      sheetCells.value = null
      aggregationCells.value = ''
    }

    const deleteAggregationCellItem = (index: number) => {
      aggregationCellItems.value.splice(index, 1)
    }

    const variables = computed<AddAggregationMutationVariables>(() => ({
      periodId: props.period.id,
      aggregationCell: sheetCell.value ? transformation(sheetCell.value.name, aggregationCell.value) : '',
      aggregationMethod: aggregationKind.value ? aggregationKind.value.value : '',
      aggregationCells: aggregationCellItems.value
    }))

    const close = () => {
      sheetCell.value = null
      aggregationCell.value = ''
      sheetCells.value = null
      aggregationCells.value = ''
      aggregationKind.value = null
      aggregationCellItems.value = []
    }

    return {
      aggregationItems,
      aggregationKind,
      addAggregationMutation,
      aggregationCell,
      aggregationCells,
      sheetCell,
      sheetCells,
      aggregationCellItems,
      addAggregationCellItem,
      deleteAggregationCellItem,
      variables,
      close
    }
  }
})
</script>
