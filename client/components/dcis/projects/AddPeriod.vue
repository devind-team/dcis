<template lang="pug">
  mutation-modal-form(
    :header="$t('dcis.projects.addPeriod.header')"
    :subheader="project.name"
    :button-text="$t('dcis.projects.addPeriod.buttonText')"
    :mutation="addPeriod"
    :variables="{ name, file, projectId: project.id }"
    :update="addPeriodUpdate"
    mutation-name="addPeriod"
    i18n-path="dcis.projects.addPeriod"
    persistent
    @close="close"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      validation-provider(v-slot="{ errors, valid }" :name="$t('dcis.projects.addPeriod.name')" rules="required|min:3|max:250")
        v-text-field(v-model="name" :label="$t('dcis.projects.addProject.name')" :error-messages="errors" :success="valid")
      validation-provider(v-slot="{ errors, valid }" :name="$t('dcis.projects.addPeriod.file')" rules="required")
        v-file-input(v-model="file" :label="$t('dcis.projects.addPeriod.file')" :error-messages="errors" :success="valid")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType, Ref } from '#app'
import { defineComponent, ref } from '#app'
import { AddPeriodMutationPayload, ProjectType } from '~/types/graphql'
import addPeriod from '~/gql/dcis/mutations/project/add_period.graphql'
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
    const name: Ref<string> = ref<string>('')
    const file: Ref<File | null> = ref<File | null>(null)

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
    return { name, file, addPeriod, addPeriodUpdate, close }
  }
})
</script>
