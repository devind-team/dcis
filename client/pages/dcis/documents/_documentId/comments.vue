<template lang="pug">
left-navigator-container(:bread-crumbs="bc" @update-drawer="$emit('update-drawer')")
  pre {{ comments }}
  v-row(justify="center" )
    div(class="view messages")
      section(class="chat-box")
        v-divider
        div(v-for="message in state.messages"
          :key="message.key"
          :class="(message.username === state.username ? 'message current-user' : 'message')")
          div(class="message-inner")
            div(class="username") {{ message.username }}
            div(class="content") {{ message.content }}
            div(class="time" align="right") {{ message.time }}
    footer(class="textarea")
      form(@submit.prevent="SendMessage")
        v-textarea(label="Введите комментарий" v-model="inputMessage" auto-grow rows="1")
        v-col(cols="3")
          v-btn(color="primary" absolute right bottom) {{ 'Отправить' }}
</template>

<script lang="ts">
import { computed, ComputedRef, defineComponent, PropType, reactive, onMounted, ref } from '#app'
import { BreadCrumbsItem } from '~/types/devind'
import { useI18n, useFilters, useCommonQuery } from '~/composables'
import LeftNavigatorContainer from '~/components/common/grid/LeftNavigatorContainer.vue'
import BreadCrumbs from '~/components/common/BreadCrumbs.vue'
import {
  DocumentCommentsQuery,
  DocumentCommentsQueryVariables
} from '~/types/graphql'
import documentCommentsQuery from '~/gql/dcis/queries/document_comments.graphql'

export default defineComponent({
  components: { LeftNavigatorContainer, BreadCrumbs },
  props: {
    breadCrumbs: { required: true, type: Array as PropType<BreadCrumbsItem[]> }
  },
  setup (props) {
    const { t, localePath } = useI18n()
    const { timeHM } = useFilters()
    const inputMessage = ref('')
    const state = reactive({
      username: '',
      messages: []
    })

    const { data: comments } = useCommonQuery<
      DocumentCommentsQuery,
      DocumentCommentsQueryVariables
    >({
      document: documentCommentsQuery
    })

    const SendMessage = () => {
      if (inputMessage.value === '' || inputMessage.value === null) {
        return
      }
      const message = {
        username: state.username,
        content: inputMessage.value,
        time: timeHM(Date())
      }
      inputMessage.value = ''
    }
    onMounted(() => {
      const data = {
        0: {
          username: 'Куратор',
          content: 'Какой-то комментарий',
          time: timeHM(Date())
        },
        1: {
          username: 'Куратор',
          content: 'Да, хорошо, вычитывайте. В названиях разделов не должно быть только английских слов. Например, ' +
            'к "3.1.5 Sentry" надо добавить русских слов, чтобы человеку не очень знакомому с программированием, ' +
            'было понятно что это.',
          time: timeHM(Date())
        }
      }
      const messages = []
      Object.keys(data).forEach((key) => {
        messages.push({
          id: key,
          username: data[key].username,
          content: data[key].content,
          time: data[key].time
        })
      })
      state.messages = messages
    })

    const bc: ComputedRef < BreadCrumbsItem[] > = computed<BreadCrumbsItem[]>(() => ([
      ...props.breadCrumbs,
      {
        text: t('dcis.documents.links.comments') as string,
        to: localePath({ name: 'dcis-documents-documentId-comments' }),
        exact: true
      }
    ]))
    return {
      bc,
      state,
      inputMessage,
      SendMessage,
      comments
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
  .message {
    display: flex;
    margin-bottom: 15px;

    .message-inner {
      .username {
        color: #888;
        font-size: 14px;
        margin-bottom: 5px;
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
        margin-bottom: 5px;
        padding-left: 15px;
        padding-right: 15px;
      }
    }
    &.current-user {
      margin-top: 30px;
      justify-content: flex-end;
      text-align: right;
      .message-inner {
        max-width: 75%;
        .content {
          color: #FFF;
          font-weight: 600;
        }
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
