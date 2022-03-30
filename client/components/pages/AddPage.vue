<template lang="pug">
  apollo-mutation(
    v-slot="{ mutate, loading, error }"
    :mutation="require('~/gql/pages/mutations/page/add_page.graphql')"
    :variables="input"
    @done="addPageDone"
    tag
  )
    validation-observer(v-slot="{ handleSubmit, invalid }" ref="addPage" tag="div")
      form(@submit.prevent="handleSubmit(mutate)")
        v-card
          v-card-title {{ $t('pages.page.add.category') }}: {{ category.text }}
          v-card-text
            v-alert(type="error" :value="!!error" dismissible) {{ error }}
            validation-provider(:name="$t('pages.page.add.avatar')" v-slot="{ errors, valid }")
              v-file-input(
                v-model="input.avatar"
                :label="$t('pages.page.add.avatar')"
                :error-messages="errors"
                :success="valid"
                prepend-icon="mdi-camera"
                show-size
              )
            validation-provider(
              :name="$t('pages.page.add.title')"
              rules="required|min:3|max:1023"
              v-slot="{ errors, valid }"
            )
              v-text-field(
                v-model="input.title"
                :label="$t('pages.page.add.title')"
                :error-messages="errors"
                :success="valid"
                clearable
              )
            v-select(
              v-model="input.kindId"
              :items="pageKindList"
              :label="$t('pages.page.add.kind')"
              :loading="$apollo.queries.pageKinds.loading"
              item-text="name"
              item-value="id"
            )
            v-row
              v-col(cols="4")
                v-checkbox(v-model="input.parallax" :label="$t('pages.page.add.parallax')")
              v-col(cols="4")
                v-checkbox(v-model="input.hide" :label="$t('pages.page.add.hide')")
              v-col(cols="4")
                v-checkbox(v-model="input.priority" :label="$t('pages.page.add.priority')")
            validation-provider(
              :name="$t('pages.page.add.tags')"
              :rules="tagAutocompleteFocus ? 'required|min:1|max:255' : ''"
              :detect-input="false"
              mode="passive"
              v-slot="{ validate, errors }"
            )
              v-autocomplete(
                v-model="input.tagNames"
                v-stream:update:search-input="searchStreamTags$"
                :items="tagList"
                :label="$t('pages.page.add.tags')"
                :loading="$apollo.queries.tags.loading"
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
            v-checkbox(v-model="addSignature" :label="$t('pages.page.add.signature')")
            validation-provider(
              v-if="addSignature"
              v-slot="{ errors, valid }"
              :name="$t('pages.page.add.signature')"
              rules="min:2|max:100"
            )
              v-text-field(
                v-model="input.signature"
                :label="$t('pages.page.add.signature')"
                :error-messages="errors"
                :success="valid"
                clearable
              )
            v-checkbox(v-model="addText" :label="$t('pages.page.add.text')")
            rich-text-editor(v-if="addText" v-model="input.text")
            v-card-actions
              v-spacer
              v-btn(:disabled="invalid" :loading="loading" type="submit" color="primary") {{ $t('pages.page.add.add') }}
</template>

<script lang="ts">
import { camelCase } from 'scule'
import { Component, Prop, Ref, Vue } from 'vue-property-decorator'
import { ValidationObserver } from 'vee-validate'
import { Subject } from 'rxjs'
import { debounceTime, filter, pluck, startWith } from 'rxjs/operators'
import {
  TagType,
  TagTypeEdge,
  PageKindType,
  AddPageMutation,
  AddPageMutationVariables,
  CategoryType,
  ErrorFieldType
} from '~/types/graphql'
import RichTextEditor from '~/components/common/editor/RichTextEditor.vue'

@Component<AddPage>({
  components: { RichTextEditor },
  computed: {
    pageKindList () {
      return [
        { id: null, name: this.$t('pages.components.addPage.common') },
        ...this.$apollo.queries.pageKinds.loading ? [] : this.pageKinds
      ]
    },
    tagList () {
      return [
        ...this.$apollo.queries.tags.loading ? [] : this.tags,
        ...this.newTags,
        ...(this.input.tagNames as string[])
          .filter((name: string) => this.tags.find((tag: TagType) => tag.name === name) === undefined)
          .filter((name: string) => this.newTags.find(tag => tag.name === name) === undefined)
          .map((name: string) => ({ name }))
      ]
    }
  },
  domStreams: ['searchStreamTags$'],
  subscriptions () {
    const searchTags$ = this.searchStreamTags$.pipe(
      pluck('event', 'msg'),
      filter((e: string | null) => e !== null),
      debounceTime(700),
      startWith('')
    )
    return { searchTags$ }
  },
  apollo: {
    tags: {
      query: require('~/gql/pages/queries/tags.graphql'),
      variables () {
        return {
          first: 5,
          search: this.searchTags$
        }
      },
      update ({ tags }: any): TagType[] {
        return tags.edges.map((e: TagTypeEdge) => e.node) as TagType[]
      },
      watchLoading (isLoading: boolean) {
        this.watchTagsLoading$.next(isLoading)
      }
    },
    pageKinds: require('~/gql/pages/queries/page_kinds.graphql')
  }
})
export default class AddPage extends Vue {
  @Prop({ required: true, type: Object }) category!: CategoryType

  @Ref() readonly addPage!: InstanceType<typeof ValidationObserver>

  addText: boolean = false
  drawer: boolean = false
  addSignature: boolean = false
  searchStreamTags$: Subject<any> = new Subject<any>()
  searchTags$: string = ''
  watchTagsLoading$: Subject<boolean> = new Subject<boolean>()
  newTagName: string = ''
  newTags: { name: string }[] = []
  tagAutocompleteFocus: boolean = false

  input!: AddPageMutationVariables
  tags!: TagType[]
  tagList!: { name: string }
  pageKinds!: PageKindType[]
  pageKindList!: { id: string | null, name: string }

  data () {
    return {
      input: {
        avatar: null,
        parallax: false,
        title: '',
        signature: null,
        kindId: null,
        hide: false,
        priority: false,
        categoryId: this.category.id,
        tagNames: [],
        text: ''
      }
    }
  }

  /**
   * Обработка изменения ввода имени тега.
   * Осуществляем валидацию, если ранее была обнаружена ошибка
   * @param errors
   * @param validate
   */
  async updateSearchInput (errors: string[], validate: (e: any) => Promise<{ valid: boolean}>): Promise<void> {
    if (errors.length !== 0) {
      await validate(this.newTagName)
    }
  }

  /**
   * Ожидание состояния загрузки тегов
   * @param loading
   */
  async waitTagsLoading (loading: boolean): Promise<boolean> {
    if (this.$apollo.queries.tags.loading === loading) {
      return loading
    } else {
      return await new Promise<boolean>((resolve) => {
        const subscription = this.watchTagsLoading$.subscribe((resultLoading) => {
          subscription.unsubscribe()
          resolve(resultLoading)
        })
      })
    }
  }

  /**
   * Добавление тега при нажатии на клавишу Enter.
   * Добавляем тег, если VAutocomplete не выполнил свое действие
   * в ответ на нажатие на клавишу Enter, и если тег правильный и не был добавлен ранее
   * @param validate
   * @param event
   */
  async addTag (validate: (e: any) => Promise<{ valid: boolean }>, event: KeyboardEvent): Promise<void> {
    await this.$nextTick()
    if (event.defaultPrevented) {
      return
    } else {
      event.preventDefault()
    }
    if (!(await validate(this.newTagName)).valid) {
      return
    }
    if ((this.input.tagNames as string[]).find(name => name === this.newTagName) !== undefined) {
      this.newTagName = ''
      return
    }
    await this.waitTagsLoading(false)
    const existingTag = this.tags.find(tag => tag.name === this.newTagName) ||
      this.newTags.find(tag => tag.name === this.newTagName)
    if (existingTag === undefined) {
      this.newTags.push({ name: this.newTagName })
      const tagNames = this.input.tagNames as string[]
      tagNames.push(this.newTagName)
    } else {
      const tagNames = this.input.tagNames as string[]
      tagNames.push(existingTag.name)
    }
    this.newTagName = ''
  }

  /**
   * Обработка окончания запроса на добавление страницы
   * @param success
   * @param errors
   * @param page
   */
  addPageDone ({ data: { addPage: { success, errors, page } } }: { data: AddPageMutation }): void {
    if (success) {
      this.$router.push(this.localePath({ name: 'pages-pageId', params: { pageId: page!.id } }))
    } else {
      this.addPage.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.$t(`pages.page.add.${camelCase(c.field)}`) as string]: c.messages }
        }, {}))
    }
  }
}
</script>
