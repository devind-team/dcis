import { Editor } from '@tiptap/core'
import { Italic as ItalicOriginal, ItalicOptions } from '@tiptap/extension-italic'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

export default class Italic extends AbstractExtension {
  constructor (options?: Partial<ItalicOptions>) {
    super(ItalicOriginal, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'italic',
          icon: 'mdi-format-italic',
          onClick: (editor: Editor) => editor.chain().focus().toggleItalic().run(),
          isActive: (editor: Editor) => editor.isActive('italic'),
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
