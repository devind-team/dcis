<template lang="pug">
mutation-modal-form(
  :header="String($t('dcis.projects.addProject.header'))"
  :button-text="String($t('dcis.projects.addProject.buttonText'))"
  :mutation="addProjectMutation"
  :variables="{ name, short, description, visibility, user: user.id, contentType: division }"
  :update="addProjectUpdate"
  mutation-name="addProject"
  i18n-path="dcis.projects.addProject"
  @close="close"
)
  template(#activator="{ on }")
    slot(name="activator" :on="on")
  template(#form)
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.projects.addProject.name'))"
      rules="required|min:3|max:250"
    )
      v-text-field(
        v-model="name"
        :label="$t('dcis.projects.addProject.name')"
        :error-messages="errors"
        :success="valid"
        autofocus
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.projects.addProject.short'))"
      rules="required|min:3|max:30"
    )
      v-text-field(
        v-model="short"
        :label="$t('dcis.projects.addProject.short')"
        :error-messages="errors"
        :success="valid"
        counter
      )
    validation-provider(
      v-slot="{ errors, valid }"
      :name="String($t('dcis.projects.addProject.description'))"
      rules="required|min:3|max:1023"
    )
      v-textarea(
        v-model="description"
        :label="$t('dcis.projects.addProject.description')"
        :error-messages="errors"
        :success="valid"
      )
    v-radio-group(v-model="division" row)
      v-radio(
        v-for="availableDivision in availableDivisions"
        :key="availableDivision"
        :label="$t(`dcis.projects.addProject.${availableDivision}`)"
        :value="availableDivision"
      )
    v-checkbox(v-model="visibility" :label="$t('dcis.projects.addProject.visibility')")
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import type { PropType } from '#app'
import { defineComponent, ref, toRef } from '#app'
import { useAuthStore } from '~/stores'
import { AddProjectMutationPayload, UserType } from '~/types/graphql'
import addProjectMutation from '~/gql/dcis/mutations/project/add_project.graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export type AddProjectMutationResult = { data: { addProject: AddProjectMutationPayload } }
type UpdateFunction = (cache: DataProxy | any, result: AddProjectMutationResult | any) => DataProxy | void

export default defineComponent({
  components: { MutationModalForm },
  props: {
    update: { type: Function as PropType<UpdateFunction>, required: true }
  },
  setup (props, { emit }) {
    const authStore = useAuthStore()

    const availableDivisions: string[] = ['organization', 'department']

    const user = toRef(authStore, 'user')
    const name = ref<string>('')
    const short = ref<string>('')
    const description = ref<string>('')
    const division = ref<string>(availableDivisions[0])
    const visibility = ref<boolean>(true)

    const close = () => {
      name.value = ''
      short.value = ''
      description.value = ''
      division.value = availableDivisions[0]
      visibility.value = true
      emit('close')
    }

    const addProjectUpdate = (cache: DataProxy, result: AddProjectMutationResult) => {
      const { success } = result.data.addProject
      if (success) {
        props.update(cache, result)
      }
    }

    return {
      user,
      name,
      short,
      description,
      division,
      visibility,
      availableDivisions,
      close,
      addProjectMutation,
      addProjectUpdate
    }
  }
})
</script>
