<template lang="pug">
  v-menu(v-model="drawer" bottom)
    template(v-slot:activator="{ on: onMenu }")
      v-tooltip(bottom)
        template(v-slot:activator="{ on: onTooltip }")
          v-btn(v-on="{...onMenu, ...onTooltip}" @click.prevent="" icon)
            v-icon {{ icon }}
        span {{ t('settings') }}
    v-list
      //- Добавление категории
      add-category(v-if="add && hasPerm('pages.add_category')"
        :category="category"
        :update="addCategoryUpdate"
        @close="drawer = false")
        template(#default="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-briefcase-plus-outline
            v-list-item-content {{ t('addSubcategory') }}
      //- Мутация на изменение аватара
      choose-avatar-dialog(@input="changeCategoryAvatar($event)")
        template(#default="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-image
            v-list-item-content {{ t('changeAvatar') }}
      //- Изменение названия
      edit-category(
        v-if="hasPerm('pages.change_category') || category.user.id === user.id"
        :category="category"
        :update="changeCategoryUpdate"
        @close="drawer = false")
        template(#default="{ on }")
          v-list-item(v-on="on")
            v-list-item-icon
              v-icon mdi-briefcase-edit-outline
            v-list-item-content {{ t('changeName') }}
      //- Удаление категории
      apollo-mutation(
        :mutation="require('~/gql/pages/mutations/category/delete_category.graphql')"
        :variables="{ categoryId: category.id}"
        :update="(store, result) => deleteCategoryUpdate(store, result, category)"
        @done="drawer = false")
        template(v-slot="{ mutate }")
          delete-menu(
            v-if="hasPerm('pages.delete_category') || category.user.id === user.id"
            @confirm="mutate"
            :itemName="t('category')"
            )
            template(v-slot:default="{ on }")
              v-list-item(v-on="on")
                v-list-item-icon
                  v-icon mdi-briefcase-remove-outline
                v-list-item-content {{ t('delete') }}
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { mapGetters } from 'vuex'
import { DataProxy } from 'apollo-cache'
import { CategoryType, UserType } from '~/types/graphql'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import AddCategory from '~/components/pages/AddCategory.vue'
import EditCategory from '~/components/pages/EditCategory.vue'
import ChooseAvatarDialog from '~/components/common/dialogs/ChooseAvatarDialog.vue'

@Component<CategoryAction>({
  components: { ChooseAvatarDialog, EditCategory, AddCategory, DeleteMenu },
  computed: {
    ...mapGetters({ user: 'auth/user', hasPerm: 'auth/hasPerm' })
  }
})
export default class CategoryAction extends Vue {
  @Prop({ default: false, type: Boolean }) add!: boolean
  @Prop({ default: 'mdi-cog' }) icon!: string
  @Prop() category!: CategoryType

  drawer: boolean = false

  user!: UserType
  hasPerm!: (permissions: string | string[], or?: boolean) => boolean

  // Callback методы для обновления cache
  @Prop() addCategoryUpdate!: (store: DataProxy, result: any) => void
  @Prop({ required: true }) changeCategoryUpdate!: (store: DataProxy, result: any) => void
  @Prop({ required: true }) deleteCategoryUpdate!: (
    store: DataProxy,
    result: any,
    category: CategoryType
  ) => void

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`pages.components.categoryAction.${path}`, values) as string
  }

  changeCategoryAvatar (avatar: File | null) {
    this.$apollo.mutate({
      mutation: require('~/gql/pages/mutations/category/change_category_avatar.graphql'),
      variables: { categoryId: this.category.id, avatar },
      update: (
        store: DataProxy,
        { data: { changeCategoryAvatar } }
      ) => this.changeCategoryUpdate(
        store,
        { data: { changeCategory: changeCategoryAvatar } }
      )
    })
    this.drawer = false
  }
}
</script>
