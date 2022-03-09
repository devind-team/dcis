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
import { Vue, Component, Prop, VModel } from 'vue-property-decorator'
import { PropType } from 'vue'
import { UserType } from '~/types/graphql'
import { Item, MultipleMessageFunction } from '~/types/filters'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'
import QueryDataFilter from '~/components/common/filters/QueryDataFilter.vue'
import AvatarDialog from '~/components/users/AvatarDialog.vue'

@Component<UsersDataFilter>({
  inheritAttrs: false,
  components: { ItemsDataFilter, QueryDataFilter, AvatarDialog }
})
export default class UsersDataFilter extends Vue {
  @Prop({ type: Array as PropType<Item[]> }) readonly users?: Item[]

  @Prop({
    type: String,
    default () {
      return (this as any).$options.methods.t.call(this, 'title')
    }
  }) readonly title!: string

  @Prop({
    type: String,
    default () {
      return (this as any).$options.methods.t.call(this, 'noFiltrationMessage')
    }
  }) readonly noFiltrationMessage!: string

  @Prop({
    type: Function as PropType<MultipleMessageFunction>,
    default (name: string, restLength: number): string {
      return (this as any).$tc('core.filters.usersFilter.multipleMessage', restLength, { name, restLength })
    }
  }) readonly multipleMessageFunction!: MultipleMessageFunction

  @VModel({ type: [Object, Array] as PropType<Item | Item[]> })
  readonly selectedValue!: Item | Item[] | null | undefined

  /**
   * Поиск пользователя
   * @param user
   * @param search
   * @return
   */
  searchUser (user: UserType, search: string): boolean {
    return [this.$getUserName(user), this.$getUserFullName(user)].some(
      v => v.toLocaleLowerCase().includes(search.toLocaleLowerCase())
    )
  }

  /**
   * Получение перевода относильно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`core.filters.usersFilter.${path}`, values) as string
  }
}
</script>
