import { Editor } from '@tiptap/core'
import { Color } from '@tiptap/extension-color'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ColorPicker from '~/components/common/editor/extensions/actions/toolbar/ColorPicker.vue'

export default class FontColor extends AbstractExtension {
  constructor () {
    super(Color, undefined)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'fontColor',
          icon: 'mdi-format-color-text',
          onClick: (editor: Editor, options: string) => {
            if (options === '#00000000') {
              editor.chain().focus().unsetColor().run()
            } else {
              editor.chain().focus().setColor(options).run()
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
