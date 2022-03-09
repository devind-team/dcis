import { Link, LinkOptions } from '@tiptap/extension-link'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import FileUploadDialog from '~/components/common/editor/extensions/nativeExtensions/file/FileUploadDialog.vue'

export default class File extends AbstractExtension {
  constructor (options?: Partial<LinkOptions>) {
    super(Link, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'file',
          icon: 'mdi-file',
          onClick: () => undefined,
          isActive: () => false,
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: FileUploadDialog
        }
      }
    ]
  }
}
