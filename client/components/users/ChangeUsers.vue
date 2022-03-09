<template lang="pug">
  v-autocomplete(
    v-model="selectedUsers"
    v-stream:update:search-input="searchStreamUsers$"
    v-bind="$attrs"
    :items="users"
    :loading="$apollo.queries.users.loading"
    :filter="filterUsers"
    :label="$t('ac.users.components.changeUsers.users')"
    item-text="name"
    item-value="id"
    multiple
    clearable
    return-object
    hide-no-data
    hide-selected
  )
    template(#selection="{ item }")
      v-chip(@click:close="selectedUsers.splice(selectedUsers.indexOf(item), 1)" close)
        avatar-dialog(:item="item" left)
        | {{ item.lastName }} {{ item.firstName }} {{ item.sirName }}
    template(#item="{ item }")
      v-list-item-avatar
        avatar-dialog(:item="item")
      v-list-item-content
        v-list-item-title {{ item.lastName }} {{ item.firstName }} {{ item.sirName }}
        v-list-item-subtitle {{ item.username }}
</template>

<script lang="ts">
import Vue from 'vue'
import { Subject } from 'rxjs'
import { debounceTime, filter, pluck, startWith } from 'rxjs/operators'
import { UserType } from '~/types/graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'

export default Vue.extend<any, any, any, any>({
  components: { AvatarDialog },
  props: {
    initUsers: { type: Array, required: true },
    value: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    searchStreamUsers$: new Subject(),
    searchUsers$: ''
  }),
  computed: {
    selectedUsers: {
      get (): boolean {
        return this.value
      },
      set (value: UserType[]) {
        this.$emit('input', value)
      }
    }
  },
  domStreams: ['searchStreamUsers$'],
  subscriptions () {
    // @ts-ignore
    const searchUsers$ = this.searchStreamUsers$.pipe(
      pluck('event', 'msg'),
      filter((e: any) => e !== null),
      debounceTime(700),
      startWith('')
    )
    return { searchUsers$ }
  },
  apollo: {
    users: {
      query: require('~/gql/eleden/queries/core/search_users.graphql'),
      variables () { return { first: this.searchUsers$ ? undefined : 10, search: this.searchUsers$ } },
      update ({ users }) {
        return [...this.initUsers, ...users.edges.map((e: { node?: UserType }) => e.node)]
      }
    }
  },
  methods: {
    /**
     * Фильтрация пользователей
     * @param item
     * @param queryText
     * @return
     */
    filterUsers (item: UserType, queryText: string): boolean {
      const qt = queryText.toLocaleLowerCase()
      const ln = item.lastName.toLocaleLowerCase()
      const fn = item.firstName.toLocaleLowerCase()
      const sn = item.sirName?.toLocaleLowerCase()
      return ln.includes(qt) || fn.includes(qt) || item.username.includes(qt) || (Boolean(sn) && qt.includes(sn!))
    }
  }
})
</script>
