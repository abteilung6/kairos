import { useObjectStoreListQuery } from 'api/objectStores'
import { useNavigate } from 'react-router-dom'
import { Routes } from 'utils/routes'

// TODO: extract table component with filter, sort
const ObjectStoreListPage: React.FC = () => {
  const navigate = useNavigate()
  const objectStoreListQuery = useObjectStoreListQuery()
  const objectStores = objectStoreListQuery.data ?? []

  return (
    <div>
      <h1>ObjectStoreListPage</h1>
      {objectStoreListQuery.isError && (
        <div>{objectStoreListQuery.error.message}</div>
      )}
      <div>
        <button onClick={() => navigate(Routes.OBJECT_STORE_CREATE_PAGE)}>
          Create Object
        </button>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>URL</th>
          </tr>
        </thead>
        <tbody>
          {objectStores.map(({ id, object_key, bucket_get_url }) => {
            return (
              <tr key={id}>
                <td>{id}</td>
                <td>
                  <a
                    href={bucket_get_url ?? ''}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {object_key}
                  </a>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export default ObjectStoreListPage
