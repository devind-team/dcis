<template lang="pug">
  bread-crumbs(:items="bc")
    apollo-mutation(
      v-slot="{ mutate, loading, error }"
      :mutation="require('~/gql/dcis/mutations/project/change_project.graphql')"
      :variables="{ id: project.id, name,  short, description, visibility, archive }"
      :update="changeProjectUpdate"
      tag
    )
      v-card
        v-card-title
          v-app-bar-nav-icon(v-if="$vuetify.breakpoint.smAndDown" @click="$emit('update-drawer')")
          | {{ $t('dcis.projects.changeProject.header') }}
        v-card-subtitle {{ project.name }}
        validation-observer(v-slot="{ handleSubmit, invalid }" tag="div")
          form(@submit.prevent="handleSubmit(mutate)")
            v-card-text
              v-alert(type="success" :value="successUpdate") {{ $t('mutationSuccess') }}
              v-alert(type="error" :value="!!error" dismissible) {{ $t('mutationBusinessLogicError', { error: error }) }}
              validation-provider(
                v-slot="{ errors, valid }"
                :name="String($t('dcis.projects.addProject.name'))"
                rules="required|min:3|max:250"
              )
                v-text-field(
                  v-model="name"
                  :label="$t('dcis.projects.addProject.name')"
                  :error-messages="errors" :success="valid"
                  counter
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
                  counter
                )
              v-row
                v-col(cols="12" md="2")
                  v-checkbox(v-model="visibility" :label="$t('dcis.projects.addProject.visibility')")
                v-col(cols="12" md="10")
                  v-checkbox(v-model="archive" :label="$t('dcis.projects.changeProject.archive')")
            v-card-actions
              v-btn(
                v-if="project.user && project.user.id === user.id || hasPerm('dcis.change_project')"
                :disabled="invalid"
                :loading="loading"
                type="submit"
                color="success"
              ) {{ $t('dcis.projects.changeProject.save') }}
        v-divider
        v-card-title Удаление проекта
        v-card-text
          v-alert(type="warning") {{ $t('dcis.projects.changeProject.warning') }}
        v-card-actions
          apollo-mutation(
            v-slot="{ mutate }"
            :mutation="require('~/gql/dcis/mutations/project/delete_project.graphql')"
            :variables="{ id: project.id}"
            @done="deleteProjectDone"
            tag
          )
            delete-menu(
              v-if="project.user && project.user.id === user.id || hasPerm('dcis.delete_project')"
              v-slot="{ on }"
              :itemName="String($t('dcis.projects.changeProject.deleteItemName'))"
              @confirm="mutate"
            )
              v-btn(v-on="on" color="error") {{ $t('dcis.projects.changeProject.delete') }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { promiseTimeout } from '@vueuse/core'
import type { ComputedRef, PropType, Ref } from '#app'
import { computed, defineComponent, toRefs, useRoute, useRouter, ref, inject } from '#app'
import {
  ChangeProjectMutationPayload,
  DeleteProjectMutationPayload,
  ProjectType,
  UserType
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import { useI18n } from '~/composables'
import type { HasPermissionFnType } from '~/store'
import { useAuthStore } from '~/store'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

type ChangeProjectResultMutation = { data: { changeProject: ChangeProjectMutationPayload } }
type DeleteProjectResultMutation = { data: { deleteProject: DeleteProjectMutationPayload } }
type ChangeProjectUpdateType = (cache: DataProxy, result: ChangeProjectResultMutation) => DataProxy

export default defineComponent({
  components: { BreadCrumbs, DeleteMenu },
  middleware: 'auth',
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    const authStore = useAuthStore()
    const { localePath } = useI18n()
    const router = useRouter()
    const route = useRoute()
    const { user, hasPerm } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(authStore)

    const changeUpdate: ChangeProjectUpdateType = inject<ChangeProjectUpdateType>('changeUpdate')

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Настройки', to: localePath({ name: 'dcis-projects-projectId-settings' }), exact: true }
    ]))
    const name: Ref<string> = ref<string>(props.project.name)
    const short: Ref<string> = ref<string>(props.project.short)
    const description: Ref<string> = ref<string>(props.project.description)
    const visibility: Ref<boolean> = ref<boolean>(props.project.visibility)
    const archive: Ref<boolean> = ref<boolean>(props.project.archive)
    const successUpdate: Ref<boolean> = ref<boolean>(false)

    const changeProjectUpdate = (cache: DataProxy, result: ChangeProjectResultMutation) => {
      const { success } = result.data.changeProject
      if (success) {
        changeUpdate(cache, result)
        successUpdate.value = true
        promiseTimeout(5000).then(() => (successUpdate.value = false))
      }
    }

    const deleteProjectDone = ({ data: { deleteProject: { success } } }: DeleteProjectResultMutation) => {
      if (success) {
        router.push(localePath({ name: 'dcis-projects', query: { projectId: route.params.projectId } }))
      }
    }

    return {
      bc,
      name,
      short,
      description,
      visibility,
      archive,
      successUpdate,
      user,
      hasPerm,
      changeProjectUpdate,
      deleteProjectDone
    }
  }
})
</script>
