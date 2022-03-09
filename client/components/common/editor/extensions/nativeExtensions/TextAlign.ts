import { Editor } from '@tiptap/core'
import { TextAlign as TextAlignOriginal, TextAlignOptions } from '@tiptap/extension-text-align'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

export default class TextAlign extends AbstractExtension {
  constructor (options?: Partial<TextAlignOptions>) {
    super(TextAlignOriginal, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'align.left',
          icon: 'mdi-format-align-left',
          onClick: (editor: Editor) => editor.chain().focus().setTextAlign('left').run(),
          isActive: (editor: Editor) => editor.isActive({ textAlign: 'left' }),
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'align.center',
          icon: 'mdi-format-align-center',
          onClick: (editor: Editor) => editor.chain().focus().setTextAlign('center').run(),
          isActive: (editor: Editor) => editor.isActive({ textAlign: 'center' }),
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'align.right',
          icon: 'mdi-format-align-right',
          onClick: (editor: Editor) => editor.chain().focus().setTextAlign('right').run(),
          isActive: (editor: Editor) => editor.isActive({ textAlign: 'right' }),
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'align.justify',
          icon: 'mdi-format-align-justify',
          onClick: (editor: Editor) => editor.chain().focus().setTextAlign('justify').run(),
          isActive: (editor: Editor) => editor.isActive({ textAlign: 'justify' }),
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
