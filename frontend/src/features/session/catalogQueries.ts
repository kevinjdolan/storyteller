import { useQuery } from '@tanstack/react-query'
import {
  fetchGenreCatalog,
  fetchToneCatalogForGenre,
} from '../../api/catalog.ts'

export const catalogQueryKeys = {
  all: ['catalog'] as const,
  genres: () => [...catalogQueryKeys.all, 'genres'] as const,
  tones: (genreSlug: string) =>
    [...catalogQueryKeys.all, 'genres', genreSlug, 'tones'] as const,
}

export function useGenreCatalogQuery() {
  return useQuery({
    queryKey: catalogQueryKeys.genres(),
    queryFn: fetchGenreCatalog,
    staleTime: 5 * 60_000,
  })
}

export function useToneCatalogQuery(genreSlug: string | null | undefined) {
  return useQuery({
    queryKey: catalogQueryKeys.tones(genreSlug ?? 'unselected'),
    queryFn: () => fetchToneCatalogForGenre(genreSlug ?? ''),
    enabled: genreSlug != null && genreSlug.length > 0,
    staleTime: 5 * 60_000,
  })
}
