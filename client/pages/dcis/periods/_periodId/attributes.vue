<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  template(#header) {{ $t('dcis.periods.links.attributes') }}
    v-spacer
    add-attribute-menu(
      v-slot="{ on, attrs}"
      :period="period"
      :from-file-update="resetUpdate"
      :add-update="addAttributeUpdate"
    )
      v-btn(v-on="on" v-bind="attrs" color="primary") {{ $t('dcis.attributes.adds') }}
  v-data-table(
    :headers="headers"
    :items="attributes"
    :loading="loading"
    disable-pagination
    disable-filtering
    disable-sort
    hide-default-footer
  )
    template(#item.action="{ item }")
      change-attribute(v-slot="{ on: onChange }" :attribute="item" :update="changeAttributeUpdate")
        v-tooltip(bottom)
          template(#activator="{ on: onTooltip, attrs}")
            v-btn(v-on="{...onTooltip, ...onChange}" v-bind="attrs" color="primary" icon)
              v-icon mdi-pencil
          span {{ $t('dcis.attributes.change') }}
      delete-menu(v-slot="{ on: onConfirm }" @confirm="deleteAttribute(item)")
        v-tooltip(bottom)
          template(#activator="{ on: onTooltip, attrs}")
            v-btn(v-on="{...onTooltip, ...onConfirm}" v-bind="attrs" color="error" icon)
              v-icon mdi-delete
          span {{ $t('dcis.attributes.delete') }}
</template>

<script lang="ts">
import type { ComputedRef, PropType } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import { useCommonQuery, useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import {
  AttributesQuery,
  AttributesQueryVariables, AttributeType, DeleteAttributeMutation,
  DeleteAttributeMutationInput,
  DeleteAttributeMutationPayload,
  PeriodType
} from '~/types/graphql'
import attributesQuery from '~/gql/dcis/queries/attributes.graphql'
import deleteAttributeMutation from '~/gql/dcis/mutations/attributes/delete_attribute.graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import AddAttributeMenu from '~/components/dcis/attributes/AddAttributeMenu.vue'
import { AddAttributeMutationResult } from '~/components/dcis/attributes/AddAttribute.vue'
import ConfirmMenu from '~/components/common/menu/ConfirmMenu.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import ChangeAttribute, { ChangeAttributeMutationResult } from '~/components/dcis/attributes/ChangeAttribute.vue'

export default defineComponent({
  components: { ChangeAttribute, DeleteMenu, ConfirmMenu, AddAttributeMenu, LeftNavigatorContainer },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.periods.links.attributes') as string,
        to: localePath({ name: 'dcis-periods-periodId-attributes' }),
        exact: true
      }
    ]))

    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => {
      const result: DataTableHeader[] = [
        { text: t('dcis.attributes.tableHeaders.name') as string, value: 'name', width: '40%' },
        { text: t('dcis.attributes.tableHeaders.placeholder') as string, value: 'placeholder', width: '25%' },
        { text: t('dcis.attributes.tableHeaders.key') as string, value: 'key', width: '10%' },
        { text: t('dcis.attributes.tableHeaders.default') as string, value: 'default', width: '15%' }
      ]
      if (props.period.canChangeAttributes) {
        result.push({ text: t('dcis.attributes.tableHeaders.action') as string, value: 'action', width: '20%' })
      }
      return result
    })

    const {
      data: attributes,
      addUpdate,
      changeUpdate,
      deleteUpdate,
      loading,
      resetUpdate
    } = useCommonQuery<AttributesQuery, AttributesQueryVariables, 'attributes'>({
      document: attributesQuery,
      variables: () => ({
        periodId: props.period.id
      })
    })

    const deleteAttribute = (attribute: AttributeType) => {
      useMutation<DeleteAttributeMutation, DeleteAttributeMutationInput>(deleteAttributeMutation, {
        update: (cache, result: { data: { deleteAttribute: DeleteAttributeMutationPayload } }) => {
          if (result.data.deleteAttribute.success) {
            deleteUpdate(cache, { data: { deleteAttribute: { id: attribute.id } } })
          }
        }
      }).mutate({ attributeId: attribute.id })
    }

    const addAttributeUpdate = (cache, result: AddAttributeMutationResult) => {
      if (!result.data.addAttribute.errors.length) {
        addUpdate(cache, result, 'attribute', false)
      }
    }

    const changeAttributeUpdate = (cache, result: ChangeAttributeMutationResult) => {
      if (!result.data.changeAttribute.errors.length) {
        changeUpdate(cache, result, 'attribute')
      }
    }

    return {
      bc,
      headers,
      attributes,
      loading,
      resetUpdate,
      changeAttributeUpdate,
      addAttributeUpdate,
      deleteAttribute
    }
  }
})
</script>
