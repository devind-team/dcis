import { Editor } from '@tiptap/core'
import { OrderedList as OrderedListOriginal, OrderedListOptions } from '@tiptap/extension-ordered-list'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

export default class OrderedList extends AbstractExtension {
  constructor (options?: Partial<OrderedListOptions>) {
    super(OrderedListOriginal, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'orderedList',
          icon: 'mdi-format-list-numbered',
          onClick: (editor: Editor) => editor.chain().focus().toggleOrderedList().run(),
          isActive: (editor: Editor) => editor.isActive('orderedList'),
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: ToolbarButton
        }
      }
    ]
  }
}
