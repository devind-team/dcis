<template lang="pug">
  mutation-form(
    @done="addPageDone"
    :mutation="require('~/gql/pages/mutations/page/add_page.graphql')"
    :variables="{ avatar, parallax, title, signature, kindId, hide, priority, categoryId: category.id, tagNames, text }"
    :header="`${$t('pages.page.add.category')}: ${category.text}`"
    :button-text="String($t('pages.page.add.add'))"
    mutation-name="addPage"
    i18n-path="pages.page.add"
  )
    template(#form)
      validation-provider(:name="String($t('pages.page.add.avatar'))" v-slot="{ errors, valid }")
        v-file-input(
          v-model="avatar"
          :label="$t('pages.page.add.avatar')"
          :error-messages="errors"
          :success="valid"
          prepend-icon="mdi-camera"
          show-size
        )
      validation-provider(
        :name="String($t('pages.page.add.title'))"
        rules="required|min:3|max:1023"
        v-slot="{ errors, valid }"
      )
        v-text-field(
          v-model="title"
          :label="$t('pages.page.add.title')"
          :error-messages="errors"
          :success="valid"
          clearable
        )
      v-select(
        v-model="kindId"
        :items="pageKindList"
        :label="$t('pages.page.add.kind')"
        :loading="pageKindsLoading"
        item-text="name"
        item-value="id"
      )
      v-row
        v-col(cols="4")
          v-checkbox(v-model="parallax" :label="$t('pages.page.add.parallax')")
        v-col(cols="4")
          v-checkbox(v-model="hide" :label="$t('pages.page.add.hide')")
        v-col(cols="4")
          v-checkbox(v-model="priority" :label="$t('pages.page.add.priority')")
      validation-provider(
        :name="String($t('pages.page.add.tags'))"
        :detect-input="false"
        mode="passive"
        v-slot="{ validate, errors }"
      )
        v-autocomplete(
          v-model="tagNames"
          :items="tagList"
          :label="$t('pages.page.add.tags')"
          :loading="tagLoading"
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
          @keydown.enter="addTag(validate, $event)"
        )
      v-checkbox(v-model="addSignature" :label="$t('pages.page.add.signature')")
      validation-provider(
        v-if="addSignature"
        v-slot="{ errors, valid }"
        :name="String($t('pages.page.add.signature'))"
        rules="min:2|max:100"
      )
        v-text-field(
          v-model="signature"
          :label="$t('pages.page.add.signature')"
          :error-messages="errors"
          :success="valid"
          clearable
        )
      v-checkbox(v-model="addText" :label="$t('pages.page.add.text')")
      rich-text-editor(v-if="addText" v-model="text")
</template>

<script lang="ts">
import { PropType } from '#app'
import { AddPageMutation, CategoryType, PageKindsQuery, PageKindsQueryVariables, TagType } from '~/types/graphql'
import pageKindsQuery from '~/gql/pages/queries/page_kinds.graphql'
import tagsQuery from '~/gql/pages/queries/tags.graphql'
import RichTextEditor from '~/components/common/editor/RichTextEditor.vue'
import MutationForm from '~/components/common/forms/MutationForm.vue'

export default defineComponent({
  components: { MutationForm, RichTextEditor },
  props: {
    category: { type: Object as PropType<CategoryType>, required: true }
  },
  setup () {
    const router = useRouter()
    const { t, localePath } = useI18n()
    const { data: pageKinds, loading: pageKindsLoading } = useCommonQuery<PageKindsQuery, PageKindsQueryVariables>({ document: pageKindsQuery })
    const pageKindList = computed<{ id: null | string | number }[]>(() => ([
      { id: null, name: t('pages.components.addPage.common') as string },
      ...pageKindsLoading.value ? [] : pageKinds.value
    ]))

    const { search: newTagName, debounceSearch } = useDebounceSearch()
    const { data: tags, loading: tagLoading } = useQueryRelay({
      document: tagsQuery,
      variables: () => ({
        search: debounceSearch.value
      })
    }, {
      pagination: useCursorPagination({ pageSize: 10 })
    })
    const newTags = ref<{ name: string }[]>([])
    const tagAutocompleteFocus = ref<boolean>(false)

    const tagList = computed(() => ([
      ...tagLoading.value ? [] : tags.value,
      ...newTags.value,
      ...(tagNames.value as string[])
        .filter((name: string) => tags.value.find((tag: TagType) => tag.name === name) === undefined)
        .filter((name: string) => newTags.value.find((tag: TagType) => tag.name === name) === undefined)
        .map((name: string) => ({ name }))
    ]))

    const addText = ref<boolean>(false)
    const drawer = ref<boolean>(false)
    const addSignature = ref<boolean>(false)

    const avatar = ref<File | null>(null)
    const parallax = ref<boolean>(false)
    const title = ref<string>('')
    const signature = ref<string | null>(null)
    const kindId = ref<number | null>(null)
    const hide = ref<boolean>(false)
    const priority = ref<boolean>(false)
    const tagNames = ref<string[]>([])
    const text = ref<string>('')

    const addTag = async (validate: (e: any) => Promise<{ valid: boolean }>, event: KeyboardEvent): Promise<void> => {
      if (event.defaultPrevented) { return } else { event.preventDefault() }
      if (!(await validate(newTagName.value)).valid) { return }
      if ((tagNames.value as string[]).find(name => name === newTagName.value) !== undefined) {
        newTagName.value = ''
        return
      }
      const existingTag = tags.value.find(tag => tag.name === newTagName.value) ||
        newTags.value.find(tag => tag.name === newTagName.value)
      if (existingTag) {
        tagNames.value.push(existingTag.name)
      } else {
        newTags.value.push({ name: newTagName.value })
        tagNames.value.push(newTagName.value)
      }
      newTagName.value = ''
    }

    const updateSearchInput = async (errors: string[], validate: (e: any) => Promise<{ valid: boolean }>): Promise<void> => {
      if (!errors.length) {
        await validate(newTagName.value)
      }
    }

    const addPageDone = ({ data: { addPage: { errors, page } } }: { data: AddPageMutation }) => {
      if (!errors.length) {
        router.push(localePath({ name: 'pages-pageId', params: { pageId: page!.id } }))
      }
    }

    return {
      pageKinds,
      pageKindList,
      pageKindsLoading,
      newTagName,
      newTags,

      tagAutocompleteFocus,
      tagLoading,
      tagList,

      addText,
      drawer,
      addSignature,

      avatar,
      parallax,
      title,
      signature,
      kindId,
      hide,
      priority,
      tagNames,
      text,
      addTag,
      updateSearchInput,
      addPageDone
    }
  }
})
</script>
