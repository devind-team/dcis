<template lang="pug">
  v-menu(bottom left)
    template(#activator="{ on }")
      slot(:on="on")
    v-list
      experimental-dialog(v-slot="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-microsoft-excel
          v-list-item-content {{ $t('ac.users.components.unloadUsersMenu.uploadToExcel') }}
      experimental-dialog(v-slot="{ on }")
        v-list-item(v-on="on")
          v-list-item-icon
            v-icon mdi-file-delimited
          v-list-item-content {{ $t('ac.users.components.unloadUsersMenu.uploadToCsv') }}
</template>

<script lang="ts">
import { defineComponent } from '#app'
import ExperimentalDialog from '~/components/common/dialogs/ExperimentalDialog.vue'

export default defineComponent({
  components: { ExperimentalDialog }
})
</script>
