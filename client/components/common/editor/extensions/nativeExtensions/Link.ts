import { Editor } from '@tiptap/core'
import { Link as LinkOriginal, LinkOptions } from '@tiptap/extension-link'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import LinkInsertDialog from '~/components/common/editor/extensions/nativeExtensions/link/LinkInsertDialog.vue'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

const LinkExtension = LinkOriginal.extend({
  addAttributes () {
    return {
      ...this.parent?.(),
      name: {
        default: null
      }
    }
  }
})

export default class Link extends AbstractExtension {
  constructor (options?: Partial<LinkOptions>) {
    super(LinkExtension, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'insertLink',
          icon: 'mdi-link-variant-plus',
          onClick: (editor: Editor, { src, label, target }: { src: string, label:string, target: string }) =>
            editor.chain().focus().insertContent(`<a href="${src}" target="${target}">${label}</a>`).run(),
          isActive: () => false,
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: LinkInsertDialog
        }
      }
    ]
  }

  get bubbleActions () {
    return [
      {
        render: {
          tooltip: 'removeLink',
          icon: 'mdi-link-variant-remove',
          onClick: (editor: Editor) =>
            editor.chain().focus().unsetLink().run(),
          isActive: () => false,
          IsDisabled: () => false,
          isVisible: (editor: Editor) => editor.isActive('link')
        },
        component: {
          type: ToolbarButton
        }
      }
    ]
  }
}
