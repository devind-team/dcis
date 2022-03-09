import { Editor } from '@tiptap/core'
import { Heading as HeadingOriginal, HeadingOptions } from '@tiptap/extension-heading'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

export default class Heading extends AbstractExtension {
  constructor (options?: Partial<HeadingOptions>) {
    super(HeadingOriginal, options)
  }

  get toolbarActions () {
    return this.options.levels.map((level: 1 | 2 | 3 | 4 | 5 | 6) => ({
      render: {
        tooltip: `h${level}`,
        icon: `mdi-format-header-${level}`,
        onClick: (editor: Editor) => editor.chain().focus().toggleHeading({ level }).run(),
        isActive: (editor: Editor) => editor.isActive('heading', { level }),
        IsDisabled: () => false,
        isVisible: () => true
      },
      component: {
        type: ToolbarButton
      }
    }))
  }
}
