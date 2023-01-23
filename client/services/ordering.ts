export const collectOrderBy = (sortBy: string[], sortDesc: boolean[]): string[] => {
  return sortBy.reduce(
    (acc: string[], item: string, index: number) => [...acc, sortDesc[index] ? `-${item}` : `${item}`],
    []
  )
}
