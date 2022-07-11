<template lang="pug">
v-menu(v-model="drawer" bottom)
  template(v-slot:activator="{ on: onMenu }")
    v-tooltip(bottom)
      template(v-slot:activator="{ on: onTooltip }")
        v-btn(v-on="{...onMenu, ...onTooltip}" @click.prevent="" icon)
          v-icon {{ icon }}
      span {{ $t('pages.components.categoryAction.settings') }}
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
          v-list-item-content {{ $t('pages.components.categoryAction.addSubcategory') }}
    //- Мутация на изменение аватара
    choose-avatar-dialog(@input="changeCategoryAvatar($event)")
      template(#default="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-image
          v-list-item-content {{ $t('pages.components.categoryAction.changeAvatar') }}
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
          v-list-item-content {{ $t('pages.components.categoryAction.changeName') }}
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
          :itemName="String($t('pages.components.categoryAction.category'))"
        )
          template(v-slot:default="{ on }")
            v-list-item(v-on="on")
              v-list-item-icon
                v-icon mdi-briefcase-remove-outline
              v-list-item-content {{ $t('pages.components.categoryAction.delete') }}
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataProxy } from 'apollo-cache'
import type { PropType, Ref } from '#app'
import { defineComponent, ref, toRefs } from '#app'
import { HasPermissionFnType, useAuthStore } from '~/stores'
import {
  CategoryType,
  ChangeCategoryAvatarMutation,
  ChangeCategoryAvatarMutationVariables,
  UserType
} from '~/types/graphql'
import changeCategoryAvatarMutation from '~/gql/pages/mutations/category/change_category_avatar.graphql'
import {
  AddCategoryMutationResult,
  ChangeCategoryMutationResult,
  DeleteCategoryMutationResult
} from '~/pages/categories/index.vue'
import DeleteMenu from '~/components/common/menu/DeleteMenu.vue'
import AddCategory from '~/components/pages/AddCategory.vue'
import EditCategory from '~/components/pages/EditCategory.vue'
import ChooseAvatarDialog from '~/components/common/dialogs/ChooseAvatarDialog.vue'

export default defineComponent({
  components: { ChooseAvatarDialog, EditCategory, AddCategory, DeleteMenu },
  props: {
    addCategoryUpdate: {
      type: Function as PropType<(cache: DataProxy, result: AddCategoryMutationResult) => void>,
      default: null
    },
    changeCategoryUpdate: {
      type: Function as PropType<(cache: DataProxy, result: ChangeCategoryMutationResult) => void>,
      required: true
    },
    deleteCategoryUpdate: {
      type: Function as PropType<(cache: DataProxy, result: DeleteCategoryMutationResult, category: CategoryType) => void>,
      required: true
    },
    category: { type: Object as PropType<CategoryType>, required: true },
    add: { type: Boolean, default: false },
    icon: { type: String, default: 'mdi-cog' }
  },
  setup (props) {
    const authStore = useAuthStore()

    const { user, hasPerm } = toRefs<{ user: UserType, hasPerm: HasPermissionFnType }>(authStore)
    const drawer: Ref<boolean> = ref<boolean>(false)

    const changeCategoryAvatar = (avatar: File | null) => {
      const { mutate } = useMutation<ChangeCategoryAvatarMutation, ChangeCategoryAvatarMutationVariables>(changeCategoryAvatarMutation, {
        update: (cache, result) => props.changeCategoryUpdate(cache as any, { data: { changeCategory: result.data as any } })
      })
      mutate({ categoryId: props.category.id, avatar }).then(() => (drawer.value = false))
    }

    return { drawer, user, hasPerm, changeCategoryAvatar }
  }
})
</script>
