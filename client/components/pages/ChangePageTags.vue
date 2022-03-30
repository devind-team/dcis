<template lang="pug">
  v-dialog(v-model="drawer" width="600")
    template(#activator="{ on }")
      slot(:on="on")
    apollo-mutation(
      v-slot="{ mutate, loading, error }"
      :mutation="require('~/gql/pages/mutations/page/change_page_tags.graphql')"
      :variables="{ pageId: page.id, tagNames }"
      @done="changePageTagsDone"
    )
      validation-observer(v-slot="{ handleSubmit, invalid }" ref="changePageTags")
        form(@submit.prevent="handleSubmit(mutate)")
          v-card
            v-card-title {{ $t('pages.page.changeTags.header') }}
              v-spacer
              v-btn(@click="close" icon)
                v-icon mdi-close
            v-card-text
              v-alert(type="error" :value="!!error" dismissible) {{ error }}
              validation-provider(
                :name="$t('pages.page.changeTags.tags')"
                :rules="tagAutocompleteFocus ? 'required|min:1|max:255' : ''"
                :detect-input="false"
                mode="passive"
                v-slot="{ validate, errors }"
              )
                v-autocomplete(
                  v-model="tagNames"
                  v-stream:update:search-input="searchStreamTags$"
                  :items="tagList"
                  :label="$t('pages.page.changeTags.tags')"
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
            v-card-actions
              v-spacer
              v-btn(
                :loading="loading"
                type="submit"
                color="primary"
              ) {{ $t('pages.page.changeTags.change') }}
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
  ChangePageTagsMutation,
  ErrorFieldType, PageType
} from '~/types/graphql'

@Component<ChangePageTags>({
  computed: {
    tagList () {
      return [
        ...this.tags,
        ...this.newTags,
        ...(this.tagNames as string[])
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
    }
  }
})
export default class ChangePageTags extends Vue {
  @Prop({ required: true, type: Object }) readonly page!: PageType

  @Ref() readonly changePageTags!: InstanceType<typeof ValidationObserver>

  drawer: boolean = false
  searchStreamTags$: Subject<any> = new Subject<any>()
  searchTags$: string = ''
  watchTagsLoading$: Subject<boolean> = new Subject<boolean>()
  newTagName: string = ''
  newTags: { name: string }[] = []
  tagAutocompleteFocus: boolean = false

  tagNames!: string[]
  tags!: TagType[]
  tagList!: { name: string }

  data () {
    return {
      tagNames: this.page.tags.map(tag => tag!.name)
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
    if ((this.tagNames as string[]).find(name => name === this.newTagName) !== undefined) {
      this.newTagName = ''
      return
    }
    await this.waitTagsLoading(false)
    const existingTag = this.tags.find(tag => tag.name === this.newTagName) ||
      this.newTags.find(tag => tag.name === this.newTagName)
    if (existingTag === undefined) {
      this.newTags.push({ name: this.newTagName })
      const tagNames = this.tagNames as string[]
      tagNames.push(this.newTagName)
    } else {
      const tagNames = this.tagNames as string[]
      tagNames.push(existingTag.name)
    }
    this.newTagName = ''
  }

  /**
   * Обработка окончания запроса на изменение тегов страницы
   * @param success
   * @param errors
   */
  changePageTagsDone ({ data: { changePageTags: { success, errors } } }: { data: ChangePageTagsMutation }): void {
    if (success) {
      this.close()
    } else {
      this.changePageTags.setErrors(errors.reduce(
        (a: { [key: string]: string[] }, c: ErrorFieldType) => {
          return { ...a, [this.$t(`pages.page.changeTags.${camelCase(c.field)}`) as string]: c.messages }
        }, {}))
    }
  }

  /**
   * Закрытие окна изменения тегов страницы
   */
  close (): void {
    this.drawer = false
    this.tagNames = this.page.tags.map(tag => tag!.name)
    this.newTags = []
    this.$nextTick(() => { this.changePageTags.reset() })
    this.$emit('close')
  }
}
</script>
