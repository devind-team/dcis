import { Editor } from '@tiptap/core'
import { Highlight as HighlightOriginal, HighlightOptions } from '@tiptap/extension-highlight'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ColorPicker from '~/components/common/editor/extensions/actions/toolbar/ColorPicker.vue'

export default class Highlight extends AbstractExtension {
  constructor (options?: Partial<HighlightOptions>) {
    super(HighlightOriginal.extend({ priority: 1000 }), options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'highlight',
          icon: 'mdi-marker',
          onClick: (editor: Editor, options: string) => {
            if (options === '#00000000') {
              editor.chain().focus().unsetHighlight().run()
            } else {
              editor.chain().focus().setHighlight({ color: options }).run()
            }
          },
          isActive: () => false,
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: ColorPicker
        }
      }
    ]
  }
}
