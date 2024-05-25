import { render } from '@testing-library/react'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

export const customRender = (children: React.ReactNode) => {
  const queryClient = new QueryClient()
  return render(
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}
