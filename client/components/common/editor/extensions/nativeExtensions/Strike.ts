import { Editor } from '@tiptap/core'
import { Strike as StrikeOriginal, StrikeOptions } from '@tiptap/extension-strike'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

export default class Strike extends AbstractExtension {
  constructor (options?: Partial<StrikeOptions>) {
    super(StrikeOriginal, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'strike',
          icon: 'mdi-format-strikethrough',
          onClick: (editor: Editor) => editor.chain().focus().toggleStrike().run(),
          isActive: (editor: Editor) => editor.isActive('strike'),
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
