<template lang="pug">
  v-progress-circular.mx-auto(v-if="$apollo.queries.userInformation.loading" indeterminate color="primary")
  v-container(v-else)
    template(v-if="userInformation")
      v-card
        v-card-title {{ $getUserFullName(userInformation) }}
        v-card-subtitle
          a(:href="`mailto: ${userInformation.email}`") {{ userInformation.email }}
        v-card-text
          v-row
            v-col(cols="12" md="3") {{ $t('profile.me.userAvatar') }}
            v-col(cols="12" md="9" align="center")
              avatar-dialog(:item="userInformation" size="300")
          profile-information(:viewUser="userInformation")
    v-row(v-else)
      v-col
        v-alert(type="warning") Пользователь скрыл информацию о себе.
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { mapGetters } from 'vuex'
import { MetaInfo } from 'vue-meta'
import { DataProxy } from 'apollo-cache'
import { UserType } from '~/types/graphql'
import AvatarDialog from '~/components/users/AvatarDialog.vue'
import ProfileInformation from '~/components/profile/ProfileInformation.vue'
import { FilterMessages } from '~/types/filters'
import ItemsDataFilter from '~/components/common/filters/ItemsDataFilter.vue'

@Component<UserIndex>({
  components: { AvatarDialog, ProfileInformation, ItemsDataFilter },
  computed: mapGetters({ user: 'auth/user', hasPerm: 'auth/hasPerm' }),
  apollo: {
    userInformation: {
      query: require('~/gql/users/queries/user.graphql'),
      variables () {
        return { userId: this.$route.params.user_id }
      }
    }
  },
  head (): MetaInfo {
    return { title: this.userInformation ? this.$getUserFullName(this.userInformation) : 'Пользователь скрыт' }
  }
})
export default class UserIndex extends Vue {
  @Prop({ required: false, type: String, default: () => ('') }) search!: string

  readonly user!: UserType

  articlesYears!: number[]
  userInformation!: UserType

  page: number = 1
  pageSize: number = 15
  selectYears: { id: number }[] = []
  totalCount: number = 0

  /**
   * Получение перевода относительно локального пути
   * @param path
   * @param values
   * @return
   */
  t (path: string, values: any = undefined): string {
    return this.$t(`articles.${path}`, values) as string
  }

  /**
   * Обновление после удаления публикации
   * @param store
   * @param success
   * @param article
   */
  deleteArticleUpdate (store: DataProxy, { data: { deleteArticle: { success } } }: any, article: ArticleType) {
    if (success) {
      const data: any = store.readQuery({ query: articlesQuery, variables: this.articlesVariables })
      data.articles.edges = data.articles.edges.filter((e: any) => e.node.id !== article.id)
      --data.articles.totalCount
      store.writeQuery({ query: articlesQuery, variables: this.articlesVariables, data })
    }
  }

  /**
   * Получение сообщений для фильтра
   * @param filterName
   * @param multiple
   * @return
   */
  getFilterMessages (filterName: string, multiple: boolean = false): FilterMessages {
    return {
      title: this.t(`general.filters.${filterName}.title`),
      noFiltrationMessage: this.t(`general.filters.${filterName}.noFiltrationMessage`),
      multipleMessageFunction: multiple
        ? (name, restLength) =>
            this.$tc(`general.filters.${filterName}.multipleMessage`, restLength, { name, restLength })
        : undefined
    }
  }
}
</script>
