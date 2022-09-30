<template lang="pug">
v-card(v-if="!profilesValueLoading && !profilesLoading" flat)
  v-row(v-for="profile in profiles" :key="profile.id")
    v-col(cols="12" md="3") {{ profile.name }}
    v-col(cols="12" md="9")
      v-data-table(
        :headers="headers"
        :items="profile.children"
        hide-default-footer
        disable-pagination
      )
        template(#item.value="{ item }")
          template(v-if="pvs[item.code]")
            template(v-if="pvs[item.code].kind === 'bool'")
              | {{ pvs[item.code].value === 'true' ? $t('yes') : $t('no') }}
            template(v-else-if="pvs[item.code].kind === 'choice'")
              | {{ choicesTypes[item.code].find(x => x.value === pvs[item.code].value).text }}
            span(v-else) {{ pvs[item.code].value }}
            v-tooltip(v-if="change" bottom)
              template(#activator="{ on }")
                v-btn(v-on="on" icon @click="changeProfileVisibility(pvs[item.code])")
                  v-icon mdi-{{ pvs[item.code].visibility ? 'eye' : 'eye-off' }}
              span {{pvs[item.code].visibility ? $t('profile.visible') : $t('profile.invisible')}}
          span.font-italic(v-else) {{ $t('notFilled') }}
          template(v-if="change")
            text-menu(
              v-if="kindTypes[item.kind] === 'text'"
              :value="pvs[item.code] ? pvs[item.code].value : ''"
              @update="changeProfileValue(item, $event)"
              multiline
            )
              template(v-slot:default="{ on: onMenu }")
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip }")
                    v-btn(v-on="{...onMenu, ...onTooltip }" left icon)
                      v-icon mdi-pencil
                  span {{ $t('change') }}
            date-menu(
              v-else-if="kindTypes[item.kind] === 'date'"
              :value="pvs[item.code] ? pvs[item.code].value : ''"
              @update="changeProfileValue(item, $event)"
            )
              template(v-slot:default="{ on: onMenu }")
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip }")
                    v-btn(v-on="{...onMenu, ...onTooltip }" left icon)
                      v-icon mdi-pencil
                  span {{ $t('change') }}
            select-menu(
              v-else-if="kindTypes[item.kind] === 'bool'"
              :items="boolTypes"
              :value="pvs[item.code] ? pvs[item.code].value : 'true'"
              @update="changeProfileValue(item, $event)"
            )
              template(v-slot:default="{ on: onMenu }")
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip }")
                    v-btn(v-on="{...onMenu, ...onTooltip }" left icon)
                      v-icon mdi-pencil
                  span {{ $t('change') }}
            select-menu(
              v-else-if="kindTypes[item.kind] === 'choice'"
              :items="choicesTypes[item.code]"
              :value="pvs[item.code] ? pvs[item.code].value : choicesTypes[item.code][0].value"
              @update="changeProfileValue(item, $event)"
            )
              template(v-slot:default="{ on: onMenu }")
                v-tooltip(bottom)
                  template(#activator="{ on: onTooltip }")
                    v-btn(v-on="{...onMenu, ...onTooltip }" left icon)
                      v-icon mdi-pencil
                  span {{ $t('change') }}
v-progress-circular(v-else color="primary" indeterminate)
</template>

<script lang="ts">
import { useMutation } from '@vue/apollo-composable'
import { DataTableHeader } from 'vuetify/types'
import { computed, defineComponent, toRefs } from '#app'
import type { ComputedRef, PropType } from '#app'
import {
  ProfilesQuery,
  ProfilesQueryVariables,
  ProfilesValueQuery,
  ProfilesValueQueryVariables,
  ProfileValueType,
  ChangeProfileValueMutation,
  ChangeProfileValueMutationVariables,
  ChangeProfileVisibilityMutation,
  ChangeProfileVisibilityMutationVariables,
  UserType,
  ProfileType
} from '~/types/graphql'
import { useCommonQuery, useI18n } from '~/composables'
import { useAuthStore } from '~/stores'
import TextMenu from '~/components/common/menu/TextMenu.vue'
import DateMenu from '~/components/common/menu/DateMenu.vue'
import SelectMenu from '~/components/common/menu/SelectMenu.vue'
import profilesQuery from '~/gql/core/queries/profiles.graphql'
import profilesValueQuery from '~/gql/core/queries/profiles_value.graphql'
import changeProfileValueMutation from '~/gql/core/mutations/profile/change_profile_value.graphql'
import changeProfileVisibilityMutation from '~/gql/core/mutations/profile/change_profile_visibility.graphql'

export type ProfileAggregation = {
  [code: string]: ProfileValueType & { kind: string }
}

/**
 * Типы возможных значений
 */
const kindTypes: { [key: string]: string } = {
  A_0: 'text',
  A_1: 'date',
  A_2: 'bool',
  A_3: 'file',
  A_4: 'choice'
}

export default defineComponent({
  components: { TextMenu, DateMenu, SelectMenu },
  middleware: 'auth',
  props: {
    viewUser: { type: Object as PropType<UserType>, required: true }
  },
  setup (props) {
    const { t } = useI18n()
    const userStore = useAuthStore()
    const { hasPerm, user } = toRefs(userStore)

    const {
      loading: profilesLoading,
      data: profiles
    } = useCommonQuery<ProfilesQuery, ProfilesQueryVariables>({
      document: profilesQuery
    })

    const {
      loading: profilesValueLoading,
      data: profilesValue,
      changeUpdate,
      update
    } = useCommonQuery<ProfilesValueQuery, ProfilesValueQueryVariables>({
      document: profilesValueQuery,
      variables: () => ({
        userId: props.viewUser.id
      })
    })

    const { mutate: ChangeProfileValueMutate } = useMutation<ChangeProfileValueMutation, ChangeProfileValueMutationVariables>(
      changeProfileValueMutation,
      {
        update: (cache, result) => update(cache, result, (dataCache, { data: { changeProfileValue: { profileValue } } }) => {
          const dataKey: string = Object.keys(dataCache)[0]
          dataCache[dataKey] = dataCache[dataKey].filter((e: ProfileValueType) => e.profile.id !== profileValue.profile.id)
          dataCache[dataKey].push(profileValue)
          return dataCache
        })
      }
    )

    const changeProfileValue = (profile: ProfileType, newValue: string): void => {
      ChangeProfileValueMutate({ userId: props.viewUser.id, profileId: profile.id, value: newValue })
    }

    const { mutate: ChangeProfileVisibilityMutate } = useMutation<ChangeProfileVisibilityMutation, ChangeProfileVisibilityMutationVariables>(
      changeProfileVisibilityMutation,
      { update: (cache, result) => changeUpdate(cache, result, 'profileValue') }
    )

    const changeProfileVisibility = (profileValue: ProfileValueType): void => {
      ChangeProfileVisibilityMutate({ visibility: !profileValue.visibility, profileValueId: profileValue.id })
    }

    const headers: ComputedRef<DataTableHeader[]> = computed<DataTableHeader[]>(() => ([
      { text: t('profile.tableHeaders.name') as string, value: 'name', width: '45%' },
      { text: t('profile.tableHeaders.value') as string, value: 'value', width: '55%' }
    ]))
    const boolTypes: ComputedRef = computed(() => ([
      { text: t('yes') as string, value: 'true' },
      { text: t('no') as string, value: 'false' }
    ]))
    const choicesTypes: ComputedRef = computed(() => ({
      gender: [
        { text: t('profile.male') as string, value: '0' },
        { text: t('profile.female') as string, value: '1' }
      ]
    }))
    const change: ComputedRef<boolean> = computed<boolean>(() => (
      hasPerm.value('devind_core.change_profilevalue') || user.value.id === props.viewUser.id
    ))

    const pvs: ComputedRef<ProfileAggregation> = computed<ProfileAggregation>(() => (
      profilesValue.value.reduce((a, c) => {
        return Object.assign({ [c.profile.code]: { ...c, kind: kindTypes[c.profile.kind] } }, a)
      }, {})
    ))

    return {
      profilesLoading,
      profilesValueLoading,
      profiles,
      profilesValue,
      headers,
      kindTypes,
      boolTypes,
      choicesTypes,
      change,
      pvs,
      changeProfileValue,
      changeProfileVisibility
    }
  }
})
</script>
