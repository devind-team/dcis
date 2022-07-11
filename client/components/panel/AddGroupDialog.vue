<template lang="pug">
v-dialog(v-model="dialog" width="600")
  template(v-slot:activator="{ on }")
    v-btn(v-on="on" color="primary") {{ $t('add') }}
  v-card
    v-card-title {{ $t('ac.teams.addMenu.addForm.header') }}
    v-card-text
      ValidationObserver(v-slot="{ invalid }" ref="addGroup")
        ValidationProvider(:name="$t('index.name')" rules="required|min:2" v-slot="{ errors, valid }")
          v-text-field(v-model="name" :label="$t('index.name')" :success="valid" :error-messages="errors")
        v-select(
          v-model="selectGroup"
          :items="groups"
          item-text="name"
          item-value="id"
          :label="$t('panel.permissionFrom')"
          clearable
          )
        v-row
          v-col(cols="12" md="6")
            v-btn(@click="dialog = false" color="warning") {{ $t('cancel') }}
          v-col.text-right(cols="12" md="6")
            v-btn(@click="addGroup" :disabled="invalid" color="success") {{ $t('add') }}
</template>

<script lang="ts">
import Vue from 'vue'
import groupsQuery from '~/gql/core/queries/groups.graphql'
import { ErrorFieldType } from '~/types/graphql'

export default Vue.extend<any, any, any, any>({
  data: () => ({
    name: '',
    selectGroup: null,
    dialog: false
  }),
  apollo: {
    groups: groupsQuery
  },
  methods: {
    /**
     * Функция для добавления группы пользователей
     */
    async addGroup (): Promise<void> {
      await this.$apollo.mutate({
        mutation: require('~/gql/core/mutations/group/add_group.graphql'),
        variables: { name: this.name, permissionFrom: this.selectGroup },
        update: (store: any, { data: { addGroup: { success, errors, group } } }: any) => {
          if (success) {
            const data: any = store.readQuery({ query: groupsQuery })
            data.groups = [...data.groups, group]
            store.writeQuery({ query: groupsQuery, data })
          } else {
            errors.forEach((e: ErrorFieldType) => {
              this.$refs.addGroup.setErrors({ [this.$t(`index.${e.field}`) as string]: e.messages })
            })
          }
        }
      })
      this.dialog = false
      this.name = ''
      this.selectGroup = null
      this.$nextTick(() => { this.$refs.addGroup.reset() })
    }
  }
})
</script>
