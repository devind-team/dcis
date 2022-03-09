import { HardBreak as HardBreakOriginal, HardBreakOptions } from '@tiptap/extension-hard-break'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'

export default class HardBreak extends AbstractExtension {
  constructor (options?: Partial<HardBreakOptions>) {
    super(HardBreakOriginal, options)
  }
}
