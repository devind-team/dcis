export type Class = string | string[] | { [key: string]: boolean }
export type Item = Record<string, any>
export type SearchFunction = (item: Item, search: string) => boolean
export type GetName = (item: Item) => string
export type MessageFunction = (selectedItems: Item[]) => string
export type MultipleMessageFunction = (name: string, restLength: number) => string
export type Variables = { [key: string]: any }
export type SearchOn = { input: (value: string) => void }
export type FilterMessages = {
  title: string,
  noFiltrationMessage: string,
  multipleMessageFunction?: MultipleMessageFunction
}
