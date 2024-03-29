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
      template(v-if="project.canChange")
        v-card-title
          v-app-bar-nav-icon(v-if="$vuetify.breakpoint.smAndDown" @click="$emit('update-drawer')")
          | {{ t('dcis.projects.changeProject.header') }}
        v-card-subtitle {{ project.name }}
        validation-observer(v-slot="{ handleSubmit, invalid }" tag="div")
          form(@submit.prevent="handleSubmit(mutate)")
            v-card-text
              v-alert(type="success" :value="successUpdate") {{ t('mutationSuccess') }}
              v-alert(
                type="error"
                :value="!!error"
                dismissible
              ) {{ t('mutationBusinessLogicError', { error: error }) }}
              validation-provider(
                v-slot="{ errors, valid }"
                :name="String(t('dcis.projects.addProject.name'))"
                rules="required|min:3|max:250"
              )
                v-text-field(
                  v-model="name"
                  :label="t('dcis.projects.addProject.name')"
                  :error-messages="errors" :success="valid"
                  counter
                )
              validation-provider(
                v-slot="{ errors, valid }"
                :name="String(t('dcis.projects.addProject.short'))"
                rules="required|min:3|max:30"
              )
                v-text-field(
                  v-model="short"
                  :label="t('dcis.projects.addProject.short')"
                  :error-messages="errors"
                  :success="valid"
                  counter
                )
              validation-provider(
                v-slot="{ errors, valid }"
                :name="String(t('dcis.projects.addProject.description'))"
                rules="required|min:3|max:1023"
              )
                v-textarea(
                  v-model="description"
                  :label="t('dcis.projects.addProject.description')"
                  :error-messages="errors"
                  :success="valid"
                  counter
                )
              v-row
                v-col(cols="12" md="2")
                  v-checkbox(v-model="visibility" :label="t('dcis.projects.addProject.visibility')")
                v-col(cols="12" md="10")
                  v-checkbox(v-model="archive" :label="t('dcis.projects.changeProject.archive')")
            v-card-actions
              v-btn(
                :disabled="invalid"
                :loading="loading"
                type="submit"
                color="success"
              ) {{ t('dcis.projects.changeProject.save') }}
      v-divider(v-if="project.canChange && project.canDelete")
      template(v-if="project.canDelete")
        v-card-title {{ t('dcis.projects.deleteProject.header') }}
        v-card-text
          v-alert(type="warning") {{ t('dcis.projects.deleteProject.warning') }}
        v-card-actions
          apollo-mutation(
            v-slot="{ mutate }"
            :mutation="require('~/gql/dcis/mutations/project/delete_project.graphql')"
            :variables="{ id: project.id}"
            @done="deleteProjectDone"
            tag
          )
            delete-menu(
              v-slot="{ on }"
              :itemName="String(t('dcis.projects.deleteProject.itemName'))"
              @confirm="mutate"
            )
              v-btn(v-on="on" color="error") {{ t('dcis.projects.deleteProject.delete') }}
</template>

<script lang="ts">
import { DataProxy } from 'apollo-cache'
import { promiseTimeout } from '@vueuse/core'
import type { PropType } from '#app'
import { computed, defineComponent, ref, inject, useNuxt2Meta } from '#app'
import { useRoute, useRouter } from '#imports'
import {
  ProjectType,
  ChangeProjectMutationPayload,
  DeleteProjectMutationPayload
} from '~/types/graphql'
import { BreadCrumbsItem } from '~/types/devind'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import { useI18n } from '~/composables'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

type ChangeProjectResultMutation = { data: { changeProject: ChangeProjectMutationPayload } }
type DeleteProjectResultMutation = { data: { deleteProject: DeleteProjectMutationPayload } }
type ChangeProjectUpdateType = (cache: DataProxy, result: ChangeProjectResultMutation) => DataProxy

export default defineComponent({
  name: 'ProjectSettings',
  components: { BreadCrumbs, DeleteMenu },
  middleware: 'auth',
  props: {
    project: { type: Object as PropType<ProjectType>, required: true },
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true }
  },
  setup (props) {
    useNuxt2Meta({ title: props.project.name })

    const { t, localePath } = useI18n()

    const router = useRouter()
    const route = useRoute()

    if (!(props.project.canChange || props.project.canDelete)) {
      router.push(localePath({ name: 'dcis-projects-projectId-periods' }))
    }

    const changeUpdate: ChangeProjectUpdateType = inject<ChangeProjectUpdateType>('changeUpdate')

    const bc = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.projects.links.settings') as string,
        to: localePath({ name: 'dcis-projects-projectId-settings' }),
        exact: true
      }
    ]))
    const name = ref<string>(props.project.name)
    const short = ref<string>(props.project.short)
    const description = ref<string>(props.project.description)
    const visibility = ref<boolean>(props.project.visibility)
    const archive = ref<boolean>(props.project.archive)
    const successUpdate = ref<boolean>(false)

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
        router.push(localePath({
          name: 'dcis-projects',
          query: { deleteProjectId: route.params.projectId }
        }))
      }
    }

    return {
      t,
      bc,
      name,
      short,
      description,
      visibility,
      archive,
      successUpdate,
      changeProjectUpdate,
      deleteProjectDone
    }
  }
})
</script>
