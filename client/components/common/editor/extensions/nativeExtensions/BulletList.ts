import { Editor } from '@tiptap/core'
import { BulletList as BulletListOriginal, BulletListOptions } from '@tiptap/extension-bullet-list'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

export default class BulletList extends AbstractExtension {
  constructor (options?: Partial<BulletListOptions>) {
    super(BulletListOriginal, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'bulletList',
          icon: 'mdi-format-list-bulleted',
          onClick: (editor: Editor) => editor.chain().focus().toggleBulletList().run(),
          isActive: (editor: Editor) => editor.isActive('bulletList'),
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
