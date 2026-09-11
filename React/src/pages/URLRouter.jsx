import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || '/api/v1/urls'

function CreateURL() {
  const [formData, setFormData] = useState({
    url: '',
    alias: '',
    expires_at: '',
  })
  const [shortUrl, setShortUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setCopied(false)
    setLoading(true)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error('Something went wrong while shortening your link.')
      }

      const data = await response.json()
      setShortUrl(data[0])
    } catch (err) {
      setError(err.message || 'Unable to reach the server. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = async () => {
    if (!shortUrl) return
    try {
      await navigator.clipboard.writeText(shortUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      setError('Could not copy to clipboard.')
    }
  }

  return (
    <main className="page">
      <header className="hero">
        <div className="brand">
          {/* <span>ShortURL</span> */}
        </div>
        <h1>Shorten links that are easy to share</h1>
        <p className="subtitle">
          Paste a long URL, add an optional alias and expiry date, and get a
          short link in seconds.
        </p>
      </header>

      <section className="card" aria-labelledby="form-heading">
        <h2 id="form-heading" className="sr-only">
          Create a short link
        </h2>
        <form onSubmit={handleSubmit} className="url-form">
          <div className="field">
            <label htmlFor="LongURL_field">Long URL</label>
            <input
              type="url"
              name="url"
              id="LongURL_field"
              placeholder="https://example.com/your-long-link"
              value={formData.url}
              onChange={handleChange}
              required
            />
          </div>

          <div className="field-row">
            <div className="field">
              <label htmlFor="CustomAlies">
                Custom alias <span className="optional">(optional)</span>
              </label>
              <input
                type="text"
                id="CustomAlies"
                name="alias"
                placeholder="my-link"
                value={formData.alias}
                onChange={handleChange}
              />
            </div>

            <div className="field">
              <label htmlFor="ExpiryDate">
                Expiry date <span className="optional">(optional)</span>
              </label>
              <input
                type="date"
                name="expires_at"
                id="ExpiryDate"
                value={formData.expires_at}
                onChange={handleChange}
              />
            </div>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Shortening…' : 'Shorten URL'}
          </button>
        </form>

        {error && (
          <p className="error-message" role="alert">
            {error}
          </p>
        )}

        {shortUrl && (
          <div className="result" role="status">
            <label htmlFor="URLData">Your short link</label>
            <div className="result-row">
              <textarea
                id="URLData"
                name="URLData"
                value={shortUrl}
                readOnly
                rows={1}
              />
              <button type="button" className="copy-btn" onClick={handleCopy}>
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
          </div>
        )}
      </section>

    </main>
  )
}

export default CreateURL