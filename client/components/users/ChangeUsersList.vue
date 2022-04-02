<template lang="pug">
  v-list(dense)
    v-autocomplete(
      v-stream:update:search-input="searchStreamUsers$"
      v-model="selectUsers"
      :label="$t('ac.users.components.changeUsers.users')"
      :items="selectUsers"
      :loading="$apollo.queries.users.loading"
      multiple clearable return-object no-filter hide-selected hide-no-data
    )
      template(v-slot:selection="{ item }")
        v-chip(@click:close="remove(item)" small close)
          avatar-dialog(:item="item" left)
          | {{ $getUserFullName(item) }}
    v-list-item(v-for="user in users" :key="user.id")
      v-list-item-avatar
        avatar-dialog(:item="user")
      v-list-item-content
        v-list-item-title {{ $getUserFullName(user) }}
        v-list-item-subtitle {{ user.username }} | {{ user.email }}
      v-list-item-action
        v-checkbox(v-model="selectUsers" :value="user" :key="user.id" dense)
</template>

<script lang="ts">
import { Subject } from 'rxjs'
import { debounceTime, filter, pluck, startWith } from 'rxjs/operators'
import { UserType } from '~/types/graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'

export default defineComponent({
  components: { AvatarDialog },
  props: {
    value: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    searchUsers$: '',
    searchStreamUsers$: new Subject<any>()
  }),
  computed: {
    selectUsers: {
      get (): boolean {
        return this.value
      },
      set (value: boolean) {
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
      variables () { return { first: 10, search: this.searchUsers$ } },
      update ({ users }) {
        return users.edges.map((e: { node?: UserType }) => e.node)
      }
    }
  },
  methods: {
    remove (user: UserType): void {
      this.selectUsers.splice(this.selectUsers.indexOf(user), 1)
    }
  }
})
</script>
