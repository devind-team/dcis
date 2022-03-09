export type Class = string | string[] | { [key: string]: boolean }
export type Item = { [key: string]: string }
export type SearchFunction = (item: Item, search: string) => boolean
export type GetName = (item: Item) => string
export type MultipleMessageFunction = (name: string, restLength: number) => string
export type Variables = { [key: string]: any }
export type SearchOn = { input: (value: string) => void }
export type FilterMessages = {
  title: string,
  noFiltrationMessage: string,
  multipleMessageFunction?: MultipleMessageFunction
}
