import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { HomePage } from './HomePage.tsx'

describe('HomePage', () => {
  it('links past-session previews into the session workspace route', () => {
    render(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>,
    )

    expect(
      screen.getByRole('link', { name: 'Open Lanterns Over Juniper Lake' }),
    ).toHaveAttribute('href', '/sessions/juniper-lake')
    expect(
      screen.getByRole('link', { name: 'Open sample workspace' }),
    ).toHaveAttribute('href', '/sessions/juniper-lake')
  })
})
