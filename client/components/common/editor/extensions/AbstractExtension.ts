import { Extension } from '@tiptap/core'
import ExtensionOptionsInterface from '~/components/common/editor/extensions/ExtensionOptionsInterface'

export type ActionType = { render: ExtensionOptionsInterface, component: { type: any } }

export default abstract class AbstractExtension {
  nativeExtension: Extension | null = null
  get toolbarActions (): ActionType[] { return [] }
  get bubbleActions (): ActionType[] { return [] }

  protected constructor (protected extensionClass: any, protected options?: any) {
    this.nativeExtension = extensionClass?.configure(options)
  }
}
