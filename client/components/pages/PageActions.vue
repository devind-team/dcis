<template lang="pug">
v-menu(v-model="active" :close-on-content-click="false" left bottom)
  template(#activator="{ on: onMenu }")
    v-tooltip(bottom)
      template(#activator="{ on: onTooltip }")
        v-btn(v-on="{...onMenu, ...onTooltip}" small icon)
          v-icon mdi-cog
      span {{ $t('pages.page.actions.settings') }}
  v-list
    //- Добавление секций
    v-menu(content-class="menu-elevation" transition="scale-transition" offset-x :close-on-content-click="false")
      template(#activator="{ on: onAdd }")
        v-list-item(v-on="onAdd" v-if="hasPerm('pages.add_section') || page.user.id === user.id")
          v-list-item-icon
            v-icon mdi-card-plus
          v-list-item-content {{ $t('pages.page.actions.addSection') }}
      v-list
        v-list-item(
          v-for="section in addSections"
          :key="section.icon"
          :to="localePath({ name: 'pages-pageId-section-add', query: { kind: section.kind } })"
        )
          v-list-item-icon
            v-icon mdi-{{ section.icon }}
          v-list-item-content
            v-list-item-title {{ section.text }}
    //- Изменение полей
    v-menu(
      v-if="hasChangePerm"
      :close-on-content-click="false"
      content-class="menu-elevation"
      transition="scale-transition"
      offset-x
    )
      template(#activator="{ on: onChange }")
        v-list-item(v-on="onChange")
          v-list-item-icon
            v-icon mdi-pencil-box-multiple
          v-list-item-content {{ $t('pages.page.actions.changeFields') }}
      v-list
        change-page-title(v-slot="{ on: onChangeTitle }" :page="page")
          v-list-item(v-on="onChangeTitle")
            v-list-item-icon
              v-icon mdi-pencil
            v-list-item-content {{ $t('pages.page.actions.changeTitle') }}
        change-page-kind(v-slot="{ on: onChangeKind }" :page="page")
          v-list-item(v-on="onChangeKind")
            v-list-item-icon
              v-icon mdi-pencil
            v-list-item-content {{ $t('pages.page.actions.changeKind') }}
        change-page-avatar(v-slot="{ on: onChangeAvatar }" :page="page")
          v-list-item(v-on="onChangeAvatar")
            v-list-item-icon
              v-icon mdi-image-edit
            v-list-item-content {{ $t('pages.page.actions.changeAvatar') }}
        change-page-tags(v-slot="{ on: onChangeTags }" :page="page")
          v-list-item(v-on="onChangeTags")
            v-list-item-icon
              v-icon mdi-tag-multiple
            v-list-item-content {{ $t('pages.page.actions.changeTags') }}
        v-list-item(@click="")
          v-list-item-icon
            v-icon mdi-folder-edit
          v-list-item-content {{ $t('pages.page.actions.changeCategory') }}
    //- Изменение свойств
    v-menu(
      v-if="hasChangePerm"
      :close-on-content-click="false"
      content-class="menu-elevation"
      transition="scale-transition"
      offset-x
    )
      template(#activator="{ on: onChange }")
        v-list-item(v-on="onChange")
          v-list-item-icon
            v-icon mdi-square-edit-outline
          v-list-item-content {{ $t('pages.page.actions.changeProperties') }}
      v-list
        apollo-mutation(
          :mutation="require('~/gql/pages/mutations/page/change_page_boolean_property.graphql')"
          :variables="{ pageId: page.id, field: 'hide', value: !page.hide }"
        )
          template(v-slot="{ mutate }")
            v-list-item(@click="mutate()")
              v-list-item-icon
                v-icon {{ page.hide ? 'mdi-eye' : 'mdi-eye-off' }}
              v-list-item-content {{ getBoolPropTitle('hide') }}
        apollo-mutation(
          :mutation="require('~/gql/pages/mutations/page/change_page_boolean_property.graphql')"
          :variables="{ pageId: page.id, field: 'priority', value: !page.priority }"
        )
          template(v-slot="{ mutate }")
            v-list-item(@click="mutate()")
              v-list-item-icon
                v-icon {{ page.priority ? 'mdi-arrow-down-bold' : 'mdi-arrow-up-bold' }}
              v-list-item-content {{ getBoolPropTitle('priority') }}
        apollo-mutation(
          :mutation="require('~/gql/pages/mutations/page/change_page_boolean_property.graphql')"
          :variables="{ pageId: page.id, field: 'parallax', value: !page.parallax }"
        )
          template(v-slot="{ mutate }")
            v-list-item(@click="mutate()")
              v-list-item-icon
                v-icon mdi-view-carousel
              v-list-item-content {{ getBoolPropTitle('parallax') }}
    apollo-mutation(
      :mutation="require('~/gql/pages/mutations/page/delete_page.graphql')"
      :variables="{ pageId: page.id }"
      @done="deletePageDone"
    )
      template(v-slot="{ mutate }")
        delete-menu(
          v-if="hasPerm('pages.delete_page')"
          v-slot="{ on }"
          :itemName="$t('pages.page.actions.deleteItemName')"
          @confirm="mutate"
          @cancel="active = false"
        )
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-delete
            v-list-item-content {{ $t('pages.page.actions.delete') }}
</template>

<script lang="ts">
import { defineComponent, ref, PropType, toRefs, computed } from '#app'
import { useRouter } from '#imports'
import { useI18n } from '~/composables'
import { HasPermissionFnType, useAuthStore } from '~/stores'
import { PageType, UserType, DeletePageMutation } from '~/types/graphql'
import ChangePageTitle from '~/components/pages/ChangePageTitle.vue'
import ChangePageKind from '~/components/pages/ChangePageKind.vue'
import ChangePageAvatar from '~/components/pages/ChangePageAvatar.vue'
import ChangePageTags from '~/components/pages/ChangePageTags.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'

export default defineComponent({
  components: {
    ChangePageTitle,
    ChangePageKind,
    DeleteMenu,
    ChangePageTags,
    ChangePageAvatar
  },
  props: { page: { type: Object as PropType<PageType>, required: true } },
  setup: function (props) {
    const { t, localePath } = useI18n()
    const router = useRouter()
    const authStore = useAuthStore()
    const { user, hasPerm } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(authStore)

    const active = ref(false)

    const hasChangePerm = computed(() => {
      return hasPerm.value('pages.change_page') || props.page.user?.id === user.value.id
    })

    const addSections = computed(() => {
      const helper = {
        kind: undefined,
        get text () {
          return t(`pages.section.names.${this.kind}`)
        }
      }
      return [
        { icon: 'text', kind: 'text' },
        { icon: 'image-multiple', kind: 'gallery' },
        { icon: 'file-send', kind: 'files' },
        { icon: 'account-group', kind: 'profiles' },
        { icon: 'play-box-outline', kind: 'sliders' },
        { icon: 'form-select', kind: 'form' },
        { icon: 'notebook', kind: 'jupyter' },
        { icon: 'file-delimited', kind: 'dataset' }
      ].map(obj => Object.setPrototypeOf(obj, helper))
    })

    /**
     * Получение заголовка булевого свойсва
     */
    const getBoolPropTitle = (prop: 'hide' | 'parallax' | 'priority') => {
      return props.page[prop]
        ? t(`pages.page.actions.${prop}.on`) as string
        : t(`pages.page.actions.${prop}.off`) as string
    }

    /**
     * Обработка окончания запроса на удаление страницы
     * @param success
     * @param errors
     */
    const deletePageDone = ({ data: { deletePage: { success } } }: { data: DeletePageMutation }) => {
      if (success) {
        active.value = false
        router.push(
          localePath({ name: 'categories-categoryId', params: { categoryId: props.page.category.id } }) // todo: удаление из кэша
        )
      }
    }

    return { active, user, hasPerm, addSections, hasChangePerm, getBoolPropTitle, deletePageDone }
  }
})
</script>

<style lang="sass" scoped>
.menu-elevation
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.35)
</style>
