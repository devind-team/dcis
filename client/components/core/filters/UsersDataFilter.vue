<template lang="pug">
component(
  :is="users ? 'ItemsDataFilter' : 'QueryDataFilter'"
  v-model="selectedValue"
  v-bind="$attrs"
  v-on="$listeners"
  :items="users"
  :title="title"
  :no-filtration-message="noFiltrationMessage"
  :multiple-message-function="multipleMessageFunction"
  :get-name="$getUserName"
  :search-function="searchUser"
)
  template(#item="{ item, getName, isSelected, change }")
    .d-flex.my-1.align-center
      v-checkbox.my-0.py-0(
        :key="item.id"
        :input-value="isSelected"
        :label="getName(item)"
        hide-details
        style="width: 210px"
        @change="change"
      )
      avatar-dialog(:item="item" size="40")
</template>

<script lang="ts">
import { defineComponent, computed, PropType } from '#app'
import { useFilters } from '~/composables'
import { UserType } from '~/types/graphql'
import { Item, MultipleMessageFunction } from '~/types/filters'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import QueryDataFilter from '~/components/common/filters/QueryDataFilter.vue'
import AvatarDialog from '~/components/users/AvatarDialog.vue'

export default defineComponent({
  components: { ItemsDataFilter, QueryDataFilter, AvatarDialog },
  inheritAttrs: false,
  props: {
    users: { type: Array as PropType<Item[]>, default: () => [] },
    title: {
      type: String,
      default () {
        return this.$t('core.filters.usersFilter.title')
      }
    },
    noFiltrationMessage: {
      type: String,
      default () {
        return this.$t('core.filters.usersFilter.noFiltrationMessage')
      }
    },
    multipleMessageFunction: {
      type: Function as PropType<MultipleMessageFunction>,
      default (name: string, restLength: number): string {
        return this.$tc('core.filters.usersFilter.multipleMessage', restLength, { name, restLength })
      }
    },
    value: { type: [Object, Array] as PropType<Item | Item[]>, default: () => undefined }
  },
  setup (props, { emit }) {
    const { getUserName, getUserFullName } = useFilters()
    const selectedValue = computed<Item | Item[] | null | undefined>({
      get: () => {
        return props.value
      },
      set: (value) => {
        emit('input', value)
      }
    })
    /**
     * Поиск пользователя
     * @param user
     * @param search
     * @return
     */
    const searchUser = (user: UserType, search: string): boolean => {
      return [getUserName(user), getUserFullName(user)].some(
        v => v.toLocaleLowerCase().includes(search.toLocaleLowerCase())
      )
    }
    return { selectedValue, searchUser }
  }
})
</script>
