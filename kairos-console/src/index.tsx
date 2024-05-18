import { createRoot } from 'react-dom/client'
import 'tailwindcss/tailwind.css'
import AppPage from 'pages/AppPage'

const container = document.getElementById('root') as HTMLDivElement
const root = createRoot(container)

root.render(<AppPage />)
