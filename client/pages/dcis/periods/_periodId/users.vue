<template lang="pug">
  left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
    template(#header) {{ period.name }}
    v-row
      v-col(cols="4")
        v-list
          v-list-item-group(v-model="selectGroup" color="primary")
            v-row(no-gutters align="center")
              v-col(cols="12" md="4" sm="2").caption
                v-subheader Группы
              v-col.text-right(cols="12" md="8" sm="10")
                v-btn(class="align-self-center mr-4" color="primary" icon text)
                  v-icon(large) mdi-plus-circle
            v-list-item(v-for="(item, index) in period.groups" :key="index" :value="item.id" @click="selectedGroup = item")
              v-list-item-title {{ item.name }}
      v-divider(vertical)
      v-col(cols="8")
        period-group-users(:value="selectedGroup" :period="period")
</template>

<script lang="ts">
import { ComputedRef, PropType, ref } from '#app'
import { computed, defineComponent, useNuxt2Meta } from '#app'
import { useI18n } from '~/composables'
import { BreadCrumbsItem } from '~/types/devind'
import { PeriodGroupType, PeriodType } from '~/types/graphql'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import PeriodGroupUsers from '~/components/dcis/periods/PeriodGroupUsers.vue'

export default defineComponent({
  components: { LeftNavigatorContainer, PeriodGroupUsers },
  middleware: 'auth',
  props: {
    breadCrumbs: { type: Array as PropType<BreadCrumbsItem[]>, required: true },
    period: { type: Object as PropType<PeriodType>, required: true }
  },
  setup (props) {
    const { localePath } = useI18n()
    useNuxt2Meta({ title: props.period.name })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      { text: 'Пользователи', to: localePath({ name: 'dcis-periods-periodId-users' }), exact: true }
    ]))
    const selectGroup = ref<number | null | undefined>(null)
    const selectedGroup = ref<PeriodGroupType>(null)
    return { bc, selectGroup, selectedGroup }
  }
})
</script>
