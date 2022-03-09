import { Editor, Extension, mergeAttributes } from '@tiptap/core'
import { Table as TableOriginal, TableOptions as TableOptionsOriginal } from '@tiptap/extension-table'
import { TableCell, TableCellOptions } from '@tiptap/extension-table-cell'
import { TableRow, TableRowOptions } from '@tiptap/extension-table-row'
import { TableHeader, TableHeaderOptions } from '@tiptap/extension-table-header'
import AbstractExtension from '~/components/common/editor/extensions/AbstractExtension'
import TableInsertDialog from '~/components/common/editor/extensions/nativeExtensions/table/TableInsertDialog.vue'
import ToolbarButton from '~/components/common/editor/extensions/actions/toolbar/ToolbarButton.vue'

interface TableOptions {
  table: Partial<TableOptionsOriginal>
  header: Partial<TableHeaderOptions>
  cell: Partial<TableCellOptions>
  row: Partial<TableRowOptions>
}

const CustomTable = TableOriginal.extend<TableOptionsOriginal>({
  renderHTML (attrs) {
    const cols: [string, { style: string }][] = []
    attrs.node.content.firstChild?.content.forEach((node) => {
      if (node.attrs.colwidth) {
        cols.push(['col', { style: `width: ${node.attrs.colwidth[0]}px` }])
      }
    })
    return [
      'table',
      mergeAttributes(this.options.HTMLAttributes, attrs.HTMLAttributes),
      ['colgroup', ...cols],
      ['tbody', 0]
    ]
  }
})

const TableExtension = Extension.create<TableOptions>({
  addExtensions () {
    return [
      CustomTable.configure(this.options?.table),
      TableHeader.configure(this.options?.header),
      TableCell.configure(this.options?.cell),
      TableRow.configure(this.options?.row)
    ]
  }
})

export default class Table extends AbstractExtension {
  constructor (options?: Partial<TableOptions>) {
    super(TableExtension, options)
  }

  get toolbarActions () {
    return [
      {
        render: {
          tooltip: 'bold',
          icon: 'mdi-table',
          onClick: (editor: Editor, options: { rows: number, cols: number, withHeaderRow: boolean }) => editor.chain()
            .focus().insertTable(options).run(),
          isActive: () => false,
          IsDisabled: () => false,
          isVisible: () => true
        },
        component: {
          type: TableInsertDialog
        }
      }
    ]
  }

  get bubbleActions () {
    return [
      {
        render: {
          tooltip: 'table.addColumnBefore',
          icon: 'mdi-table-column-plus-before',
          onClick: (editor: Editor) => editor.chain().focus().addColumnBefore().run(),
          isActive: () => false,
          IsDisabled: (editor: Editor) => !editor.can().addColumnBefore(),
          isVisible: (editor: Editor) => editor.isActive('table')
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'table.addColumnAfter',
          icon: 'mdi-table-column-plus-after',
          onClick: (editor: Editor) => editor.chain().focus().addColumnAfter().run(),
          isActive: () => false,
          IsDisabled: (editor: Editor) => !editor.can().addColumnAfter(),
          isVisible: (editor: Editor) => editor.isActive('table')
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'table.addRowBefore',
          icon: 'mdi-table-row-plus-before',
          onClick: (editor: Editor) => editor.chain().focus().addRowBefore().run(),
          isActive: () => false,
          IsDisabled: (editor: Editor) => !editor.can().addRowBefore(),
          isVisible: (editor: Editor) => editor.isActive('table')
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'table.addRowAfter',
          icon: 'mdi-table-row-plus-after',
          onClick: (editor: Editor) => editor.chain().focus().addRowAfter().run(),
          isActive: () => false,
          IsDisabled: (editor: Editor) => !editor.can().addRowAfter(),
          isVisible: (editor: Editor) => editor.isActive('table')
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'table.splitCell',
          icon: 'mdi-table-split-cell',
          onClick: (editor: Editor) => editor.chain().focus().splitCell().run(),
          isActive: () => false,
          IsDisabled: (editor: Editor) => !editor.can().splitCell(),
          isVisible: (editor: Editor) => editor.isActive('table')
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'table.mergeCells',
          icon: 'mdi-table-merge-cells',
          onClick: (editor: Editor) => editor.chain().focus().mergeCells().run(),
          isActive: () => false,
          IsDisabled: (editor: Editor) => !editor.can().mergeCells(),
          isVisible: (editor: Editor) => editor.isActive('table')
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'table.deleteRow',
          icon: 'mdi-table-row-remove',
          onClick: (editor: Editor) => editor.chain().focus().deleteRow().run(),
          isActive: () => false,
          IsDisabled: (editor: Editor) => !editor.can().deleteRow(),
          isVisible: (editor: Editor) => editor.isActive('table')
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'table.deleteColumn',
          icon: 'mdi-table-column-remove',
          onClick: (editor: Editor) => editor.chain().focus().deleteColumn().run(),
          isActive: () => false,
          IsDisabled: (editor: Editor) => !editor.can().deleteColumn(),
          isVisible: (editor: Editor) => editor.isActive('table')
        },
        component: {
          type: ToolbarButton
        }
      },
      {
        render: {
          tooltip: 'table.deleteTable',
          icon: 'mdi-table-remove',
          onClick: (editor: Editor) => editor.chain().focus().deleteTable().run(),
          isActive: () => false,
          IsDisabled: (editor: Editor) => !editor.can().deleteTable(),
          isVisible: (editor: Editor) => editor.isActive('table')
        },
        component: {
          type: ToolbarButton
        }
      }
    ]
  }
}
