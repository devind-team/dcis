import { Editor } from '@tiptap/core'
import { Bold as BoldOriginal, BoldOptions } from '@tiptap/extension-bold'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

export default class Bold extends AbstractExtension {
  constructor (options?: Partial<BoldOptions>) {
    super(BoldOriginal, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'bold',
          icon: 'mdi-format-bold',
          onClick: (editor: Editor) => editor.chain().focus().toggleBold().run(),
          isActive: (editor: Editor) => editor.isActive('bold'),
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
