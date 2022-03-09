import { Editor, Extension, SingleCommands } from '@tiptap/core'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import LineHeightAutocomplete
  from '~/components/common/editor/extensions/nativeExtensions/lineHeight/LineHeightAutocomplete.vue'

export interface LineHeightOptions {
  types: string[],
  defaultHeight: string
}

declare module '@tiptap/core' {
  interface Commands<ReturnType> {
    lineHeight: {
      setLineHeight: (height: string) => ReturnType,
      unsetLineHeight: () => ReturnType,
    }
  }
}

const LineHeightExtension = Extension.create<LineHeightOptions>({
  name: 'lineHeight',
  addOptions () {
    return {
      types: ['paragraph', 'heading'],
      defaultHeight: '1.5'
    }
  },
  addGlobalAttributes () {
    return [
      {
        types: this.options.types,
        attributes: {
          lineHeight: {
            default: this.options.defaultHeight,
            parseHTML: el => el.style.lineHeight || this.options.defaultHeight,
            renderHTML: (attrs) => {
              return attrs.lineHeight !== this.options.defaultHeight ? { style: `line-height: ${attrs.lineHeight}` } : {}
            }
          }
        }
      }
    ]
  },
  addCommands () {
    return {
      setLineHeight: (height: string) => ({ commands }: { commands: SingleCommands }) => {
        return this.options.types.every(type => commands.updateAttributes(type, { lineHeight: height }))
      },
      unsetLineHeight: () => ({ commands }: { commands: SingleCommands }) => {
        return this.options.types.every(type => commands.resetAttributes(type, 'lineHeight'))
      }
    }
  }
})

export default class LineHeight extends AbstractExtension {
  constructor (options?: Partial<LineHeightOptions>) {
    super(LineHeightExtension, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'lineHeight.title',
          icon: 'mdi-format-line-spacing',
          onClick: (editor: Editor, options: string) => {
            if (options === 'default') {
              editor.chain().focus().unsetLineHeight().run()
              return
            }
            editor.chain().focus().setLineHeight(options).run()
          },
          isActive: () => false,
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: LineHeightAutocomplete
        }
      }
    ]
  }
}
