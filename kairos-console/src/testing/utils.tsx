import { render } from '@testing-library/react'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider, createMemoryRouter } from 'react-router-dom'

export const customRender = (children: React.ReactNode) => {
  const queryClient = new QueryClient()
  const router = createMemoryRouter([
    {
      path: '/',
      element: children
    }
  ])
  return render(
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  )
}
