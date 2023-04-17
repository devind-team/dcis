<template lang="pug">
v-card
  v-card-title {{ $t('profile.files.name') }}
  v-card-text
    v-row(align="center")
      v-col(cols="12")
        v-btn(@click="addFilesHandle" color="primary")
          v-icon(left) mdi-upload
          | {{ $t('profile.files.downloadFiles') }}
    v-row
      v-col(cols="12" sm="6")
        v-text-field(v-model="search" :label="$t('search')" prepend-icon="mdi-magnify" clearable)
      v-col.text-right(cols="12" sm="6") {{ $t('profile.files.shownOf', { count, totalCount }) }}
    v-row
      v-col
       v-data-table(
          :headers="headers"
          :items="files"
          :loading="loading"
          disable-pagination
          hide-default-footer
        )
          template(#item.name="{ item }")
            a(:href="`/${item.src}`" target="__blank") {{ item.name }}
          template(#item.updated="{ item }") {{ $filters.dateTimeHM(item.updatedAt) }}
          template(#item.size="{ item }") {{ (item.size / 1024).toFixed(2) }} {{ $t('profile.files.kB') }}
          template(#item.actions="{ item }")
            text-menu(v-slot="{ on: onMenu }" :value="item.name" @update="changeFileMutate({ fileId: item.id, field: 'name', value: $event }).then()")
              v-tooltip(bottom)
                template(#activator="{ on: onTooltipEdit }")
                  v-btn(v-on="{...onMenu, ...onTooltipEdit}" icon color="success")
                    v-icon mdi-pencil
                span {{ $t('profile.files.changeName') }}
            v-btn(v-if="item.deleted" @click="changeFileMutate({ fileId: item.id, field: 'deleted', value: 'false' }).then()" icon color="warning")
              v-icon mdi-delete-restore
            v-tooltip(v-else bottom)
              template(#activator="{ on: onTooltip }")
                v-menu(bottom)
                  template(#activator="{ on: onMenu }")
                    v-btn(v-on="{...onTooltip, ...onMenu}" icon color="red")
                      v-icon mdi-delete
                  v-card
                    v-card-text {{ $t('profile.files.deletingFile') }}
                    v-card-actions
                      v-btn(
                        v-if="hasPerm('devind_core.delete_file')"
                        @click="deleteFileMutate({ fileId: item.id }).then()" color="error"
                      ) {{ $t('profile.files.delete') }}
                      v-btn(@click="changeFileMutate({ fileId: item.id, field: 'deleted', value: 'true' }).then()" color="warning") {{ $t('profile.files.delete') }}
              span {{ $t('profile.files.deleteFile') }}
</template>

<script lang="ts">
import type { DataTableHeader } from 'vuetify'
import { useMutation } from '@vue/apollo-composable'
import type { ComputedRef } from '#app'
import { computed, defineComponent, toRefs, useNuxt2Meta } from '#app'
import { useI18n, useQueryRelay, useCursorPagination, useSelectFiles, useDebounceSearch } from '~/composables'
import type { HasPermissionFnType } from '~/stores'
import { useAuthStore } from '~/stores'
import {
  AddFileMutation,
  AddFileMutationVariables,
  ChangeFileMutation,
  ChangeFileMutationVariables,
  DeleteFileMutation,
  DeleteFileMutationVariables,
  FilesQuery,
  FilesQueryVariables,
  FileType,
  UserType
} from '~/types/graphql'
import filesQuery from '~/gql/core/queries/files.graphql'
import addFile from '~/gql/core/mutations/file/add_file.graphql'
import changeFile from '~/gql/core/mutations/file/change_file.graphql'
import deleteFile from '~/gql/core/mutations/file/delete_file.graphql'
import TextMenu from '~/components/common/menu/TextMenu.vue'

export default defineComponent({
  components: { TextMenu },
  middleware: 'auth',
  setup () {
    const authStore = useAuthStore()
    const { t } = useI18n()
    const tl = (path: string, values: any = undefined): string => t(`profile.files.${path}`, values) as string
    useNuxt2Meta({ title: tl('name') })

    const { user, hasPerm } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(authStore)

    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('profile.files.tableHeaders.name') as string, value: 'name' },
      { text: t('profile.files.tableHeaders.ext') as string, value: 'ext', width: 120 },
      { text: t('profile.files.tableHeaders.updated') as string, value: 'updated' },
      { text: t('profile.files.tableHeaders.size') as string, value: 'size', width: 120 },
      { text: t('profile.files.tableHeaders.actions') as string, value: 'actions', sortable: false, width: 150 }
    ]))

    const { search, debounceSearch } = useDebounceSearch({
      callback: () => setPage(1)
    })

    const {
      loading,
      pagination: { setPage, totalCount, count },
      data,
      fetchMoreAvailable,
      fetchMoreData,
      addUpdate,
      changeUpdate,
      deleteUpdate
    } = useQueryRelay<FilesQuery, FilesQueryVariables, FileType>({
      document: filesQuery,
      variables: () => ({
        userId: user.value.id,
        nameContains: debounceSearch.value
      })
    }, {
      isScrollDown: true,
      pagination: useCursorPagination(),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    // Мутация для добавления файлов
    const { mutate: addFileMutate } = useMutation<AddFileMutation, AddFileMutationVariables>(addFile, {
      update: (cache, result) => addUpdate(cache, result)
    })
    const { select: addFilesHandle } = useSelectFiles((files: FileList) => {
      addFileMutate({ userId: user.value.id, files })
    })
    // Мутация для изменения файла
    const { mutate: changeFileMutate } = useMutation<ChangeFileMutation, ChangeFileMutationVariables>(changeFile, {
      update: (cache, result) => changeUpdate(cache, result, 'file')
    })
    // Мутация для удаления файла
    const { mutate: deleteFileMutate } = useMutation<DeleteFileMutation, DeleteFileMutationVariables>(deleteFile, {
      update: (cache, result) => deleteUpdate(cache, result)
    })

    return {
      user,
      hasPerm,
      headers,
      search,
      debounceSearch,
      loading,
      files: data,
      count,
      totalCount,
      fetchMoreAvailable,
      fetchMoreData,
      setPage,
      addFilesHandle,
      changeFileMutate,
      deleteFileMutate
    }
  }
})
</script>
