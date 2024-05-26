import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import ObjectStoreCreatePage from 'pages/objectStores/ObjectStoreCreatePage'
import ObjectStoreListPage from 'pages/objectStores/ObjectStoreListPage'
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import { Routes } from 'utils/routes'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false
    }
  }
})

export const router = createBrowserRouter([
  {
    path: Routes.OBJECT_STORE_LIST_PAGE,
    element: <ObjectStoreListPage />
  },
  {
    path: Routes.OBJECT_STORE_CREATE_PAGE,
    element: <ObjectStoreCreatePage />
  }
])

const Providers: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  )
}

export default Providers
