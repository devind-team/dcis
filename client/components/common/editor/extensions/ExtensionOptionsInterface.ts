import { Editor } from '@tiptap/core'

export type OnClickType = (editor: Editor, options?: any) => any
export type OnButtonStateChangedType = (editor : Editor) => boolean

export default interface ExtensionOptionsInterface {
  tooltip: string
  icon: string
  onClick: OnClickType
  isActive: OnButtonStateChangedType
  IsDisabled: OnButtonStateChangedType
  isVisible: OnButtonStateChangedType
}
