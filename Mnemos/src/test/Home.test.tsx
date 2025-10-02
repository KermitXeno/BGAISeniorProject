import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect } from 'vitest'
import Home from '../views/Home'

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  )
}

describe('Home Component', () => {
  it('renders welcome message', () => {
    renderWithRouter(<Home />)
    expect(screen.getByText('Welcome to Mnemos')).toBeInTheDocument()
  })

  it('renders feature cards', () => {
    renderWithRouter(<Home />)
    expect(screen.getByText('Fast Performance')).toBeInTheDocument()
    expect(screen.getByText('Mobile Ready')).toBeInTheDocument()
    expect(screen.getByText('Modern Tooling')).toBeInTheDocument()
  })

  it('renders call-to-action buttons', () => {
    renderWithRouter(<Home />)
    expect(screen.getByText('Get Started')).toBeInTheDocument()
    expect(screen.getByText('Learn More')).toBeInTheDocument()
  })
})