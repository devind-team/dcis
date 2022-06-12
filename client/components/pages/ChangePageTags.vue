<template lang="pug">
  mutation-modal-form(
    @done="changePageTagsDone"
    :mutation="require('~/gql/pages/mutations/page/change_page_tags.graphql')"
    :variables="{ pageId: page.id, tagNames }"
    :header="$t('pages.page.changeTags.header')"
    :button-text="$t('pages.page.changeTags.change')"
    mutation-name="changePageTags"
    i18n-path="pages.page.changeTags"
  )
    template(#activator="{ on }")
      slot(:on="on")
    template(#form)
      validation-provider(
        :name="$t('pages.page.changeTags.tags')"
        :rules="tagAutocompleteFocus ? 'required|min:1|max:255' : ''"
        :detect-input="false"
        mode="passive"
        v-slot="{ validate, errors }"
      )
        v-autocomplete(
          v-model="tagNames"
          :items="tagList"
          :label="$t('pages.page.changeTags.tags')"
          :loading="loading"
          :search-input.sync="newTagName"
          :error-messages="errors"
          item-text="name"
          item-value="name"
          multiple
          chips
          small-chips
          deletable-chips
          flat
          dense
          @update:search-input="updateSearchInput(errors, validate)"
          @focus="tagAutocompleteFocus = true"
          @blur="tagAutocompleteFocus = false"
          @keydown.enter="addTag(validate, $event)"
        )
</template>

<script lang="ts">
import { defineComponent, PropType, ref, computed } from '#app'
import { useQueryRelay, useDebounceSearch } from '~/composables'

import {
  TagType,
  PageType,
  TagsQueryVariables,
  TagsQuery
} from '~/types/graphql'
import MutationModalForm from '~/components/common/forms/MutationModalForm.vue'

export default defineComponent({
  components: { MutationModalForm },
  props: { page: { required: true, type: Object as PropType<PageType> } },
  setup (props, { emit }) {
    const { search: newTagName, debounceSearch } = useDebounceSearch()

    const newTags = ref<{ name: string }[]>([])
    const tagAutocompleteFocus = ref(false)
    const { data: tags, loading } = useQueryRelay<TagsQuery, TagsQueryVariables>({
      document: require('~/gql/pages/queries/tags.graphql'),
      variables: () => ({ first: 5, search: debounceSearch.value })
    })
    const tagNames = ref(props.page.tags.map(tag => tag!.name))

    const tagList = computed<{ name: string }[]>(() => {
      return [
        ...tags.value,
        ...newTags.value,
        ...(tagNames.value as string[])
          .filter((name: string) => tags.value.find((tag: TagType) => tag.name === name) === undefined)
          .filter((name: string) => newTags.value.find(tag => tag.name === name) === undefined)
          .map((name: string) => ({ name }))
      ]
    })
    /**
     * Обработка окончания запроса на изменение тегов страницы
     */
    const changePageTagsDone = () => {
      tagNames.value = props.page.tags.map(tag => tag!.name)
      newTags.value = []
      emit('close')
    }

    /**
     * Обработка изменения ввода имени тега.
     * Осуществляем валидацию, если ранее была обнаружена ошибка
     * @param errors
     * @param validate
     */
    const updateSearchInput = async (errors: string[], validate: (e: any) => Promise<{ valid: boolean}>) => {
      if (errors.length !== 0) {
        await validate(newTagName.value)
      }
    }

    /**
     * Добавление тега при нажатии на клавишу Enter.
     * Добавляем тег, если VAutocomplete не выполнил свое действие
     * в ответ на нажатие на клавишу Enter, и если тег правильный и не был добавлен ранее
     * @param validate
     * @param event
     */
    const addTag = async (validate: (e: any) => Promise<{ valid: boolean }>, event: KeyboardEvent) => {
      if (event.defaultPrevented) {
        return
      } else {
        event.preventDefault()
      }
      if (!(await validate(newTagName.value)).valid) {
        return
      }
      if ((tagNames.value as string[]).find(name => name === newTagName.value) !== undefined) {
        newTagName.value = ''
        return
      }
      // await this.waitTagsLoading(false) todo: разобраться с этим
      const existingTag = tags.value.find(tag => tag.name === newTagName.value) ||
        newTags.value.find(tag => tag.name === newTagName.value)
      if (existingTag === undefined) {
        newTags.value.push({ name: newTagName.value })
        tagNames.value.push(newTagName.value)
      } else {
        tagNames.value.push(existingTag.name)
      }
      newTagName.value = ''
    }
    return { tagNames, tagAutocompleteFocus, tagList, newTagName, loading, changePageTagsDone, addTag, updateSearchInput }
  }

})
</script>
