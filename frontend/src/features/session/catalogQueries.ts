import { useQuery } from '@tanstack/react-query'
import { fetchGenreCatalog } from '../../api/catalog.ts'

export const catalogQueryKeys = {
  all: ['catalog'] as const,
  genres: () => [...catalogQueryKeys.all, 'genres'] as const,
}

export function useGenreCatalogQuery() {
  return useQuery({
    queryKey: catalogQueryKeys.genres(),
    queryFn: fetchGenreCatalog,
    staleTime: 5 * 60_000,
  })
}
