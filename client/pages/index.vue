<template lang="pug">
v-container
  page-segment(v-if="!loading" v-for="segment in segments" :key="segment.id" :segment="segment")
  v-row(v-else)
    v-progress-circular.mt-12.mx-auto(size="60" color="primary" indeterminate)
</template>

<script lang="ts">
import { useNuxt2Meta, defineComponent, useRouter } from '#app'
import { useAuthStore } from '~/stores'
import { useCommonQuery, useI18n } from '~/composables'
import segmentsQuery from '~/gql/pages/queries/segments.graphql'
import { SegmentsQuery, SegmentsQueryVariables } from '~/types/graphql'
import PageSegment from '~/components/pages/PageSegment.vue'

export default defineComponent({
  components: { PageSegment },
  setup () {
    const authStore = useAuthStore()
    const { t, localePath } = useI18n()
    const router = useRouter()
    useNuxt2Meta({ title: t('homePage') as string })

    const { loginIn } = authStore
    if (loginIn) {
      router.push(localePath({ name: 'dcis-projects' }))
    }

    const { data: segments, loading } = useCommonQuery<SegmentsQuery, SegmentsQueryVariables>({
      document: segmentsQuery
    })
    return { segments, loading }
  }
})
</script>
