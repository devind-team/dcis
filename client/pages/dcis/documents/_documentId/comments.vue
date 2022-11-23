<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  v-row(justify="center" )
    div(class="view messages")
      section(v-if="!commentsLoading" class="chat-box")
        div(v-for="comment in comments" key="comment.user.id")
          div(class="container")
            div(v-if="comment.isNewDate" align="center")
              v-chip(small) {{ date(comment.createdAt) }}
              v-divider
            div(class="message-inner")
              div(class="username") {{ comment.user.username }}
              div(class="content") {{ comment.comment }}
              div(class="time" align="right") {{ timeHM(comment.createdAt) }}
    footer(class="textarea")
      form
        v-textarea(label="Введите комментарий" v-model="inputMessage" auto-grow rows="1")
        v-col(cols="3")
          v-btn(
            v-if="inputMessage"
            @click="addDocumentCommentMutate(addDocumentCommentVariables)"
            color="primary"
            absolute
            right
            bottom
          ) {{ 'Отправить' }}
          v-btn(v-else color="primary" absolute right bottom disabled) {{ 'Отправить' }}
</template>

<script lang="ts">
import { computed, ComputedRef, defineComponent, PropType, onMounted, ref } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n, useFilters, useQueryRelay, useCursorPagination } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import {
  AddDocumentCommentMutation, AddDocumentCommentMutationVariables,
  DocumentCommentsQuery,
  DocumentCommentsQueryVariables, DocumentType
} from '~/types/graphql'
import documentCommentsQuery from '~/gql/dcis/queries/document_comments.graphql'
import addDocumentCommentMutation from '~/gql/dcis/mutations/document/add_document_comment.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, BreadCrumbs },
  props: {
    document: { type: Object as PropType<DocumentType>, required: true },
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> },
    pageSize: { type: Number, default: 0 }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const { timeHM, date } = useFilters()
    const inputMessage = ref('')
    const pageSize = ref(5)

    const {
      data: commentsData,
      loading: commentsLoading,
      addUpdate
    } = useQueryRelay<DocumentCommentsQuery,
      DocumentCommentsQueryVariables>({
        document: documentCommentsQuery,
        variables: { documentId: props.document.id }
      },
      {
        isScrollDown: true,
        pagination: useCursorPagination({ pageSize: pageSize.value }),
        fetchScroll: typeof document === 'undefined' ? null : document
      })

    const comments = computed(() =>
      commentsData.value.reduce((newArr, currentItem, index) => {
        newArr.push({ ...currentItem, isNewDate: date(currentItem.createdAt) !== date(commentsData.value[index - 1]?.createdAt) })
        return newArr
      }, [])
    )

    const { mutate: addDocumentCommentMutate } = useMutation<AddDocumentCommentMutation,
      AddDocumentCommentMutationVariables>(
        addDocumentCommentMutation,
        {
          update: (cache, result) => {
            if (!result.data.addDocumentComment.errors.length) {
              addUpdate(cache, result, 'comment')
              inputMessage.value = ''
            }
          }
        }
      )

    const addDocumentCommentVariables = computed<AddDocumentCommentMutationVariables>(() => ({
      documentId: props.document.id,
      message: inputMessage.value
    }))

    onMounted(() => {
      const html = document.body.parentNode as HTMLHtmlElement
      html.scrollTop = html.scrollHeight
    })

    const bc: ComputedRef<BreadCrumbsItem[]> = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.documents.links.comments') as string,
        to: localePath({ name: 'dcis-documents-documentId-comments' }),
        exact: true
      }
    ]))
    return {
      bc,
      inputMessage,
      timeHM,
      date,
      comments,
      addDocumentCommentMutate,
      addDocumentCommentVariables,
      commentsLoading
    }
  }
})
</script>

<style lang="scss">
.view {
  width: 70%;
  display: flex;
  justify-content: center;
  min-height: 100vh;
}
.chat-box {
  width: 70%;
  border-radius: 24px 24px 0px 0px;
  background-color: #FFF;
  box-shadow: 0px 0px 12px rgba(100, 100, 100, 0.2);
  flex: 1 1 100%;
  padding: 30px;

  .container {
    flex-direction: row;

    .message-inner {
      .username {
        color: #333;
        font-size: 14px;
        margin-top: 10px;
        margin-bottom: 5px;
        font-weight: 700;
        padding-left: 15px;
        padding-right: 15px;
      }

      .content {
        display: inline-block;
        padding: 10px 20px;
        background-color: #F3F3F3;
        border-radius: 10px;
        color: #333;
        font-size: 16px;
        line-height: 1.2em;
        text-align: left;
      }

      .time {
        color: #888;
        font-size: 12px;
        padding-left: 15px;
        padding-right: 15px;
      }
    }
  }
}
.textarea {
  width: 70%;
  position: sticky;
  bottom: 0px;
  background-color: #FFF;
  padding: 30px;
  box-shadow: 0px 0px 12px rgba(100, 100, 100, 0.2);
  form {
    display: flex;
    input[type="text"] {
      flex: 1 1 100%;
      display: block;
      width: 100%;
      padding: 10px 15px;
      border-radius: 8px 0px 0px 8px;

      color: #333;
      font-size: 18px;
      box-shadow: 0px 0px 0px rgba(0, 0, 0, 0);
      background-color: #F3F3F3;
      transition: 0.4s;
      &::placeholder {
        color: #888;
        transition: 0.4s;
      }
    }

    input[type="submit"] {
      display: block;
      padding: 10px 15px;
      border-radius: 0px 8px 8px 0px;
      color: #FFF;
      font-size: 18px;
      font-weight: 700;
    }
  }
}
</style>
