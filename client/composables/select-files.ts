import defu from 'defu'

export type SelectFilesOption = {
  type?: 'file',
  multiple?: boolean
}
export type OnChangeSelectFiles = (files: FileList) => void

export function useSelectFiles (onChange: OnChangeSelectFiles, sfOptions: SelectFilesOption = {}) {
  const defaultOptions: SelectFilesOption = {
    type: 'file',
    multiple: true
  }
  const options = defu(sfOptions, defaultOptions)
  const select = () => {
    const input: HTMLInputElement = document.createElement<'input'>('input')
    input.type = options.type
    input.multiple = options.multiple

    input.onchange = () => onChange(input.files)
    input.click()
  }

  return { select }
}
