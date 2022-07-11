<template lang="pug">
v-card
  v-card-title {{ $t('profile.settings.index') }}
    v-spacer
    apollo-mutation(
      v-slot="{ mutate, loading }"
      :mutation="require('~/gql/core/mutations/settings/reset_settings')"
      :variables="{ userId: this.user.id }"
      :update="resetUpdate"
      tag
    )
      v-tooltip(bottom)
        template(#activator="{ on }")
          v-btn(v-on="on" @click="mutate" :loading="loading" type="submit" icon)
            v-icon mdi-backup-restore
        span {{ $t('profile.settings.reset') }}
  v-card-text(v-if="!loading")
    v-alert(type="success" :value="successReset") {{ $t('mutationReset')}}
    v-alert(type="error" :value="error" dismissible) {{ error }}
    v-row
      v-col(cols="12" md="3") {{ $t('profile.settings.personal') }}
      v-col(cols="12" md="9")
        settings-form(:settings="settings.filter(e => !e.readonly)" :changeSettingValue="changeSettingValue")
    v-row(v-if="hasPerm('devind_core.change_setting')")
      v-col(cols="12" md="3") {{ $t('profile.settings.site') }}
      v-col(cols="12" md="9")
        settings-form(:settings="settings.filter(e => e.readonly)" :changeSettingValue="changeSettingValue")
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { defineComponent, ref, Ref, toRef, useNuxt2Meta } from '#app'
import { useCommonQuery, useI18n } from '~/composables'
import { useAuthStore } from '~/stores'
import {
  SettingsQuery,
  SettingsQueryVariables,
  UserType,
  ChangeSettingsMutation,
  ChangeSettingsMutationVariables
} from '~/types/graphql'
import settingsQuery from '~/gql/core/queries/settings.graphql'
import changeSettings from '~/gql/core/mutations/settings/change_settings.graphql'
import SettingsForm from '~/components/profile/SettingsForm.vue'

export default defineComponent({
  components: { SettingsForm },
  middleware: 'auth',
  setup () {
    const { t } = useI18n()
    const userStore = useAuthStore()
    useNuxt2Meta({ title: t('profile.settings.index') as string })

    const user: Ref<UserType> = toRef(userStore, 'user')
    const { hasPerm } = userStore
    const successReset: Ref<boolean> = ref<boolean>(false)
    const error: Ref<string | null> = ref<string | null>(null)

    const {
      loading,
      data: settings,
      changeUpdate,
      resetUpdate
    } = useCommonQuery<SettingsQuery, SettingsQueryVariables>({
      document: settingsQuery
    })

    const { mutate: changeSettingsMutate } = useMutation<ChangeSettingsMutation, ChangeSettingsMutationVariables>(changeSettings, {
      update: (cache, result) => changeUpdate(cache, result, 'setting')
    })
    const changeSettingValue = (key: string, value: string): void => {
      changeSettingsMutate({ userId: user.value.id, key, value })
    }

    return { loading, user, hasPerm, settings, resetUpdate, changeSettingValue, error, successReset }
  }
})
</script>
