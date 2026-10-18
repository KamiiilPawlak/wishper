import { render, screen, fireEvent } from '@testing-library/react'
import App from './App'

test('increments the counter on click', () => {
  render(<App />)
  const button = screen.getByRole('button', { name: /count is 0/i })
  fireEvent.click(button)
  expect(screen.getByRole('button', { name: /count is 1/i })).toBeInTheDocument()
})
