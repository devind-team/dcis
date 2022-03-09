import { Extension } from '@tiptap/core'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'

const TableOfContentExtension = Extension.create({
  name: 'tableOfContent',
  addGlobalAttributes () {
    return [
      {
        types: [
          'heading'
        ],
        attributes: {
          id: {
            default: null
          }
        }
      }
    ]
  }
})

export default class TableOfContent extends AbstractExtension {
  constructor () {
    super(TableOfContentExtension, null)
  }
}
