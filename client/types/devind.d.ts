export type BreadCrumbsItem = {
  text: string
  disabled?: boolean
  to?: string
  href?: string
  exact?: boolean
}

export type LinksType = {
  title: string
  permissions?: string | string[]
  permOr?: boolean
  icon: string
  to: string
  params?: { [key: string]: string }
  color?: string
}

export type PageKindChoices = {
  TEXT: number
  GALLERY: number
  FILES: number
  PROFILES: number
  SLIDERS: number
  FORM: number
  JUPYTER: number
  DATASET: number
}

export type ErrorType = 'BusinessLogicError' | 'GraphQLError' | 'NetworkError'

export type WithTimer<T> = {
  value: T
  timerId: ReturnType<typeof setTimeout> | null
}
