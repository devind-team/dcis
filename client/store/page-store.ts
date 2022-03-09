import { defineStore } from 'pinia'
import { CategoryType } from '~/types/graphql'

export type PageStoreStateType = {
  activeCategories: CategoryType[]
}
export type PageStoreGettersType = {}
export type PageStoreActionsType = {
  setActiveCategories: (flatCategories: CategoryType[], categoriesId?: string[]) => void
}

export const usePageStore = defineStore<string, PageStoreStateType, PageStoreGettersType, PageStoreActionsType>('pageStore', {
  state: () => ({
    activeCategories: []
  }),
  actions: {
    setActiveCategories (flatCategories: CategoryType[], categoriesId: string[] = []): void {
      this.activeCategories = categoriesId ? flatCategories.filter((c: CategoryType) => categoriesId.includes(c.id)) : []
    }
  }
})
