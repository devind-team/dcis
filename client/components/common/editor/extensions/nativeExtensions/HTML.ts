import { Editor } from '@tiptap/core'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import HTMLEditDialog from '~/components/common/editor/extensions/nativeExtensions/html/HTMLEditDialog.vue'

export default class HTML extends AbstractExtension {
  constructor (options?: any) {
    super(null, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'insert',
          icon: 'mdi-xml',
          onClick: (editor: Editor, options: string) => editor.commands.setContent(options, true),
          isActive: () => false,
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: HTMLEditDialog
        }
      }
    ]
  }
}
