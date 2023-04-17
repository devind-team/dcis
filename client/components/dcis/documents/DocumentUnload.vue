<template lang="pug">
v-dialog(v-model="active" width="600")
  template(#activator="{ on, attrs }")
    slot(name="activator" :on="on" :attrs="attrs")
  v-card
    v-card-title {{ $t('dcis.documents.unloadDocument.name') }}
      v-spacer
      v-btn(@click="close" icon)
        v-icon mdi-close
    v-card-subtitle {{ $t('dcis.documents.unloadDocument.additional') }}
    v-card-text
      v-checkbox(
        v-for="param in params"
        v-model="additional"
        :key="param"
        :label="paramsTranslations[param]"
        :value="param"
        dense
      )
    v-card-actions
      v-spacer
      v-btn(
        :loading="loading"
        color="primary"
        @click="$emit('unload-document', additional)"
      ) {{ $t('dcis.documents.unloadDocument.unload') }}
</template>

<script lang="ts">
import { defineComponent, ref } from '#app'
import { UnloadDocumentMutation } from '~/types/graphql'

export type UnloadDocumentMutationResult = { data: UnloadDocumentMutation }

export default defineComponent({
  props: {
    loading: { type: Boolean, required: true }
  },
  setup (_, { emit }) {
    const { t } = useI18n()

    const active = ref<boolean>(false)

    const params: string[] = ['row_add_date', 'row_update_date', 'division_name', 'division_head', 'user']
    const additional = ref<string[]>([])

    const paramsTranslations = computed<Record<string, string>>(() => ({
      row_add_date: t('dcis.documents.unloadDocument.rowAddDate') as string,
      row_update_date: t('dcis.documents.unloadDocument.rowUpdateDate') as string,
      division_name: t('dcis.documents.unloadDocument.departmentName') as string,
      division_head: t('dcis.documents.unloadDocument.departmentHead') as string,
      user: t('dcis.documents.unloadDocument.user') as string
    }))

    const close = () => {
      active.value = false
      emit('close')
    }

    return { active, params, additional, paramsTranslations, close }
  }
})
</script>
