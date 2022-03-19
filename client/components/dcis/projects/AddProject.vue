<template lang="pug">
  mutation-modal-form(
    :header="$t('dcis.projects.addProject.header')"
    :button-text="$t('dcis.projects.addProject.buttonText')"
    :mutation="addProject"
    :variables="{ name, short, description, visibility }"
    :update="addProjectUpdate"
    mutation-name="addProject"
    i18n-path="dcis.projects.addProject"
    @close="close"
  )
    template(#activator="{ on }")
      slot(name="activator" :on="on")
    template(#form)
      validation-provider(v-slot="{ errors, valid }" :name="$t('dcis.projects.addProject.name')" rules="required|min:3|max:250")
        v-text-field(v-model="name" :label="$t('dcis.projects.addProject.name')" :error-messages="errors" :success="valid")
      validation-provider(v-slot="{ errors, valid }" :name="$t('dcis.projects.addProject.short')" rules="required|min:3|max:30")
        v-text-field(v-model="short" :label="$t('dcis.projects.addProject.short')" :error-messages="errors" :success="valid" counter)
      validation-provider(v-slot="{ errors, valid }" :name="$t('dcis.projects.addProject.description')" rules="required|min:3|max:1023")
        v-textarea(v-model="description" :label="$t('dcis.projects.addProject.description')" :error-messages="errors" :success="valid")
      v-checkbox(v-model="visibility" :label="$t('dcis.projects.addProject.visibility')")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType, Ref } from '#app'
import { defineComponent, ref } from '#app'
import { AddProjectMutationPayload } from '~/types/graphql'
import addProject from '~/gql/dcis/mutations/project/add_project.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddProjectMutationResult = { data: { addProject: AddProjectMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddProjectMutationResult | any) => DataProxy | void

export default defineComponent({
  components: { MutationModalForm },
  props: {
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props) {
    const name: Ref<string> = ref<string>('')
    const short: Ref<string> = ref<string>('')
    const description: Ref<string> = ref<string>('')
    const visibility: Ref<boolean> = ref<boolean>(true)

    const close = () => {
      name.value = ''
      short.value = ''
      description.value = ''
      visibility.value = true
    }

    const addProjectUpdate = (cache: DataProxy, result: AddProjectMutationResult) => {
      const { success } = result.data.addProject
      if (success) {
        props.update(cache, result)
      }
    }

    return { name, short, description, visibility, close, addProject, addProjectUpdate }
  }
})
</script>
