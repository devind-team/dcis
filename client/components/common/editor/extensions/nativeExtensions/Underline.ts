import { Editor } from '@tiptap/core'
import { Underline as UnderlineOriginal, UnderlineOptions } from '@tiptap/extension-underline'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

export default class Underline extends AbstractExtension {
  constructor (options?: Partial<UnderlineOptions>) {
    super(UnderlineOriginal, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'underline',
          icon: 'mdi-format-underline',
          onClick: (editor: Editor) => editor.chain().focus().toggleUnderline().run(),
          isActive: (editor: Editor) => editor.isActive('underline'),
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
