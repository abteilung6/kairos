import { render, screen } from '@testing-library/react'

import AppPage from './AppPage'

describe(AppPage.name, () => {
  it('should render the AppPage', () => {
    const { container } = render(<AppPage />)

    expect(
      screen.getByRole('heading', {
        name: 'AppPage'
      })
    ).toBeInTheDocument()

    expect(container).toBeInTheDocument()
  })
})
