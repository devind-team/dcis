<template lang="pug">
bread-crumbs(:items="breadCrumbs")
  v-card(flat)
    v-card-text
      v-row(justify="center")
        .message__view.messages
          section.message__chat-box
            div(v-for="message in messages" :key="message.id")
              .message-container
                .new-date.text-center(v-if="message.isNewDate")
                  v-divider
                  v-chip(small) {{ date(message.createdAt) }}
                .message(v-if="message.kind === 'MESSAGE'")
                  .user
                     .username {{ getUserName(message.user) }}
                     .time {{ timeHM(message.createdAt) }}
                  .content {{ message.comment }}
                .message(v-else-if="message.kind === 'STATUS'")
                  .user
                     .username {{ getUserName(message.user) }}
                     .time {{ timeHM(message.createdAt) }}
                  .status_message_content {{ message.comment }}
        footer.message__textarea
          form(@submit.prevent="addDocumentMessage")
            v-textarea(
              v-model="inputMessage"
              rows="1"
              auto-grow
              :label="$t('dcis.documents.comments.comment')"
              @keyup.enter="addDocumentMessage"
            )
            v-col(cols="3")
              v-btn(
                type="submit"
                color="primary"
                absolute
                right
                bottom
                :disabled="!inputMessage.trim()"
              ) {{ $t('dcis.documents.comments.send') }}
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from '#app'
import { useMutation } from '@vue/apollo-composable'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n, useFilters, useQueryRelay, useCursorPagination } from '~/composables'
import {
  DocumentType,
  DocumentMessagesQuery,
  DocumentMessagesQueryVariables,
  AddDocumentMessageMutation,
  AddDocumentMessageMutationVariables
} from '~/types/graphql'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import documentMessagesQuery from '~/gql/dcis/queries/document_messages.graphql'
import addDocumentMessageMutation from '~/gql/dcis/mutations/document/add_document_message.graphql'

export default defineComponent({
  components: { BreadCrumbs },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> },
    document: { type: Object as PropType<DocumentType>, required: true }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const { timeHM, date, getUserName } = useFilters()
    const inputMessage = ref<string>('')
    const pageSize = ref<number>(15)

    const {
      data: messagesData,
      addUpdate
    } = useQueryRelay<
      DocumentMessagesQuery,
      DocumentMessagesQueryVariables
    >({
      document: documentMessagesQuery,
      variables: {
        documentId: props.document.id
      }
    },
    {
      isScrollDown: false,
      fetchScrollTrigger: 300,
      pagination: useCursorPagination({ pageSize: pageSize.value }),
      fetchScroll: typeof document === 'undefined' ? null : document
    })

    const messages = computed(() => {
      const reversedDate = [...messagesData.value].reverse()
      return reversedDate.reduce((newArr, currentItem, index) => {
        newArr.push({
          ...currentItem,
          isNewDate: date(currentItem.createdAt) !== date(reversedDate[index - 1]?.createdAt)
        })
        return newArr
      }, [])
    })

    const { mutate: addDocumentMessageMutate } = useMutation<
      AddDocumentMessageMutation,
      AddDocumentMessageMutationVariables
    >(
      addDocumentMessageMutation,
      {
        update: (cache, result) => {
          if (!result.data.addDocumentMessage.errors.length) {
            addUpdate(cache, result, 'documentMessage')
            inputMessage.value = ''
          }
        }
      }
    )
    const addDocumentMessage = async () => {
      if (addDocumentMessageVariables.value.message) {
        await addDocumentMessageMutate(addDocumentMessageVariables.value)
      }
      document.documentElement.scrollTop = document.documentElement.scrollHeight
    }

    const addDocumentMessageVariables = computed<AddDocumentMessageMutationVariables>(() => ({
      documentId: props.document.id,
      message: inputMessage.value.trim(),
      kind: 'message'
    }))

    const bc = computed<BreadCrumbsItem[]>(() => ([
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
      getUserName,
      messages,
      addDocumentMessage
    }
  }
})
</script>

<style lang="sass">
.message__view
  width: 70%
  display: flex
  justify-content: center
  min-height: 80vh

.message__chat-box
  width: 70%
  border-radius: 24px 24px 0 0
  background-color: #FFF
  box-shadow: 0 0 12px rgba(100, 100, 100, 0.2)
  flex: 1 1 100%
  padding: 30px

  .message-container
    flex-direction: row
    margin: 15px 0

    .new-date
      hr
        position: relative
        top: 11.5px

    .message
      .user
        display: flex
        margin-bottom: 3px

        .username
          color: #333
          font-size: 14px
          font-weight: 700
          margin-left: 5px

        .time
          color: #888
          font-size: 12px
          margin-left: 5px

      .content
        display: inline-block
        padding: 10px 20px
        background-color: #F3F3F3
        border-radius: 10px
        color: #333
        font-size: 16px
        line-height: 1.2em
        text-align: left

      .status_message_content
        display: inline-block
        padding: 10px 20px
        background-color: #1976D2
        border-radius: 10px
        color: #F3F3F3
        font-size: 16px
        line-height: 1.2em
        text-align: left

.message__textarea
  width: 70%
  position: sticky
  bottom: 0
  background-color: #FFF
  padding: 30px
  box-shadow: 0 0 12px rgba(100, 100, 100, 0.2)

  form
    display: flex

    input[type="text"]
      flex: 1 1 100%
      display: block
      width: 100%
      padding: 10px 15px
      border-radius: 8px 0 0 8px

      color: #333
      font-size: 18px
      box-shadow: 0 0 0 rgba(0, 0, 0, 0)
      background-color: #F3F3F3
      transition: 0.4s
      &::placeholder
        color: #888
        transition: 0.4s

    input[type="submit"]
      display: block
      padding: 10px 15px
      border-radius: 0 8px 8px 0
      color: #FFF
      font-size: 18px
      font-weight: 700
</style>
