import { Node } from '@tiptap/core'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'

export interface IframeOptions {
  allowFullscreen: boolean,
  HTMLAttributes: {
    [key: string]: any
  }
}

declare module '@tiptap/core' {
  interface Commands<ReturnType> {
    iframe: {
      setIframe: (options: { src: string }) => ReturnType
    }
  }
}

const IFrameExtension = Node.create<IframeOptions>({
  name: 'Iframe',
  group: 'block',
  atom: true,

  addOptions () {
    return {
      allowFullscreen: true,
      HTMLAttributes: {
        class: 'iframe-wrapper'
      }
    }
  },

  addAttributes () {
    return {
      src: {
        default: null
      },
      frameborder: {
        default: 0
      },
      allowFullscreen: {
        default: this.options.allowFullscreen,
        parseHTML: () => {
          return {
            allowfullscreen: this.options.allowFullscreen
          }
        }
      }
    }
  },

  parseHTML () {
    return [{
      tag: 'iframe'
    }]
  },

  renderHTML ({ HTMLAttributes }) {
    return ['div', this.options.HTMLAttributes, ['iframe', HTMLAttributes]]
  },

  addCommands () {
    return {
      setIframe: (options: { src: string }) => ({ tr, dispatch }) => {
        const { selection } = tr
        const node = this.type.create(options)

        if (dispatch) {
          // @ts-ignore
          tr.replaceRangeWith(selection.from, selection.to, node)
        }

        return true
      }
    }
  }
})

export default class Iframe extends AbstractExtension {
  constructor (options?: Partial<IframeOptions>) {
    super(IFrameExtension, options)
  }
}
