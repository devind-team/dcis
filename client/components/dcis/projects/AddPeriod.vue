<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.periods.addPeriod.header'))"
  :subheader="project.name"
  :button-text="String($t('dcis.periods.addPeriod.buttonText'))"
  :mutation="addPeriod"
  :variables="{ name, file, projectId: project.id, multiple, readonlyFillColor, versioning }"
  :update="addPeriodUpdate"
  mutation-name="addPeriod"
  i18n-path="dcis.projects.addPeriod"
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.addPeriod.name'))"
      rules="required|min:3|max:250"
    )
      v-text-field(
        v-model="name"
        :label="$t('dcis.periods.addPeriod.name')"
        :error-messages="errors"
        :success="valid"
        autofocus
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.periods.addPeriod.file'))"
      rules="required"
    )
      v-file-input(
        v-model="file"
        :label="$t('dcis.periods.addPeriod.file')"
        :error-messages="errors"
        :success="valid"
      )
    v-checkbox(v-model="readonlyFillColor" :label="$t('dcis.periods.addPeriod.readonlyFillColor')")
    v-checkbox(v-model="multiple" :label="$t('dcis.periods.addPeriod.multiple')" readonly)
    v-checkbox(v-model="versioning" :label="$t('dcis.periods.addPeriod.versioning')")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { defineComponent, ref } from '#app'
import { AddPeriodMutationPayload, ProjectType } from '~/types/graphql'
import addPeriod from '~/gql/dcis/mutations/period/add_period.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddPeriodMutationResult = { data: { addPeriod: AddPeriodMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddPeriodMutationPayload | any) => DataProxy | any

export default defineComponent({
  components: { MutationModalForm },
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const name = ref<string>('')
    const file = ref<File | null>(null)
    const readonlyFillColor = ref<boolean>(false)
    const multiple = ref<boolean>(true)
    const versioning = ref<boolean>(false)

    const addPeriodUpdate = (cache: DataProxy, result: AddPeriodMutationResult) => {
      const { success } = result.data.addPeriod
      if (success) {
        props.update(cache, result)
      }
    }

    const close = () => {
      name.value = ''
      file.value = null
    }
    return { name, file, readonlyFillColor, multiple, versioning, addPeriod, addPeriodUpdate, close }
  }
})
</script>
