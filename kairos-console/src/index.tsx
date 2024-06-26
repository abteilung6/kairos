import React from 'react'
import Providers from 'Providers'
import { createRoot } from 'react-dom/client'
import 'tailwindcss/tailwind.css'

const container = document.getElementById('root') as HTMLDivElement
const root = createRoot(container)

root.render(
  <React.StrictMode>
    <Providers />
  </React.StrictMode>
)
