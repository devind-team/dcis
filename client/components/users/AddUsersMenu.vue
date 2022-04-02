<template lang="pug">
  v-menu(v-model="active" bottom)
    template(#activator="{ on }")
      slot(:on="on")
    v-list
      v-dialog(v-model="dialogFile" width="600" persistent)
        template(#activator="{ on: onDialog }")
          v-list-item(v-on="onDialog")
            v-list-item-icon
              v-icon mdi-file
            v-list-item-content {{ t('fromFile') }}
        v-card
          v-card-title {{ t('loadUsers') }}
            v-spacer
            v-btn(@click="close" icon)
              v-icon mdi-close
          v-card-text
            v-alert(v-if="!!errors" type="error")
              error-validate-dialog(:table="table" :errors="errors")
                template(#default="{ on }")
                  span(v-on="on" style="cursor: pointer") {{ t('error') }}
            apollo-mutation(
              :mutation="require('~/gql/core/mutations/user/upload_users.graphql')"
              :variables="{ file, groupsId: this.selectGroups.map((e) => Number(e.id)) }"
              :update="update"
              @done="handleDone")
              template(v-slot="{ mutate, error, loading }")
                ValidationObserver(v-slot="{ handleSubmit, invalid }" ref="uploadUsers")
                  form(@submit.prevent="handleSubmit(mutate)")
                    validation-provider(:name="String($t('panel.usersFile'))" rules="required" v-slot="{ errors, valid }")
                      v-file-input(v-model="file" :label="String($t('panel.usersFile'))" :success="valid" :error-messages="errors" accept=".xlsx,.csv/*")
                    v-select(v-model="selectGroups" :items="groups" label="Выберете группы" item-text="name" multiple return-object clearable)
                    v-row
                      v-col.text-right
                        v-btn(type="submit" color="primary" :disabled="invalid" :loading="loading") {{ t('load') }}
</template>

<script lang="ts">
import ErrorValidateDialog from '~/components/common/dialogs/ErrorValidateDialog.vue'

export default defineComponent({
  components: { ErrorValidateDialog },
  props: {
    update: { type: Function, required: true }
  },
  data: () => ({
    active: false,
    loading: false,
    dialogFile: false,
    file: null,
    selectGroups: [],
    errors: null,
    table: null
  }),
  apollo: {
    groups: require('~/gql/core/queries/groups.graphql')
  },
  methods: {
    /**
     * Получение перевода относильно локального пути
     * @param path
     * @param values
     * @return
     */
    t (path: string, values: any = undefined): string {
      return this.$t(`ac.users.components.addUsersMenu.${path}`, values) as string
    },
    handleDone ({ data: { uploadUsers: { success, errors, table } } }: any) {
      this.file = null
      if (success) {
        this.close()
      } else {
        this.errors = errors
        this.table = table
        this.$nextTick(() => { this.$refs.uploadUsers.reset() })
      }
    },
    close (): void {
      this.dialogFile = false
      this.errors = null
      this.table = null
      this.active = false
      this.$nextTick(() => { this.$refs.uploadUsers.reset() })
    }
  }
})
</script>
