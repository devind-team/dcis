import type { UserType } from '~/types/graphql'

export type SheetType = {
  id: string
  name: string
}
export type DocumentUserType = {
  id: string
  user: UserType
  active: boolean
  color: string
}
export type DocumentType = {
  id: string
  name: string
  users: DocumentUserType[]
  sheets: SheetType[]
}
