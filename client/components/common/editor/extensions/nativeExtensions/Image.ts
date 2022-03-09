import { Editor, mergeAttributes } from '@tiptap/core'
import { Image as ImageOriginal, ImageOptions } from '@tiptap/extension-image'
import { VueNodeViewRenderer } from '@tiptap/vue-2'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import ImageUploadDialog from '~/components/common/editor/extensions/nativeExtensions/image/ImageUploadDialog.vue'
import ImageView from '~/components/common/editor/extensions/nativeExtensions/image/ImageView.vue'
import ImageEditDialog from '~/components/common/editor/extensions/nativeExtensions/image/ImageEditDialog.vue'

interface ImageExtensionOptions {
  inline: boolean,
  HTMLAttributes: Record<string, any>,
  sizeModes: string[],
  defaultSizeMode: string,
  defaultSize: number
}

const ImageExtension = ImageOriginal.extend<ImageExtensionOptions>({
  name: 'image',
  draggable: true,
  addOptions () {
    return {
      ...ImageOriginal.options,
      sizeModes: ['px', '%'],
      defaultSizeMode: 'px',
      defaultSize: 100
    }
  },
  addAttributes () {
    return {
      ...this.parent?.(),
      width: {
        default: this.options.defaultSize
      },
      height: {
        default: this.options.defaultSize
      },
      keepAspectRatio: {
        default: false
      },
      sizeMode: {
        default: this.options.defaultSizeMode
      }
    }
  },
  parseHTML () {
    return [
      {
        tag: 'img[src]'
      }
    ]
  },
  renderHTML (attrs) {
    const mode = attrs.node.attrs.sizeMode
    const height = attrs.node.attrs.keepAspectRatio ? 'auto' : `${attrs.node.attrs.height}${mode}`
    const width = `${attrs.node.attrs.width}${mode}`
    const aspect = attrs.node.attrs.keepAspectRatio ? 'auto' : attrs.node.attrs.width / attrs.node.attrs.height
    const style = { style: `width:${width}; height:${height}; aspect-ratio:${aspect}` }
    return ['img', mergeAttributes(this.options.HTMLAttributes, attrs.HTMLAttributes, style)]
  },
  addNodeView () {
    return VueNodeViewRenderer(ImageView)
  }
})

export default class Image extends AbstractExtension {
  constructor (options?: Partial<ImageOptions>) {
    super(ImageExtension, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'image.image',
          icon: 'mdi-image',
          onClick: () => undefined,
          isActive: () => true,
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: ImageUploadDialog
        }
      }
    ]
  }

  get bubbleActions () {
    return [
      {
        render: {
          tooltip: '123',
          icon: 'mdi-image-edit',
          onClick: () => undefined,
          isActive: () => true,
          IsDisabled: () => false,
          isVisible: (editor: Editor) => editor.isActive('image')
        },
        component: {
          type: ImageEditDialog
        }
      }
    ]
  }
}
