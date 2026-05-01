import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import {
  Briefcase,
  ClipboardList,
  Database,
  KeyRound,
  LogOut,
  MessageSquare,
  Plus,
  RefreshCw,
  Save,
  Search,
  Settings,
  User,
  Wand2
} from 'lucide-react'
import './styles.css'

const API_BASE = '/api'

function apiRequest(path, { token, method = 'GET', body, formData } = {}) {
  const headers = {}
  if (token) headers.Authorization = `Bearer ${token}`
  if (body) headers['Content-Type'] = 'application/json'
  return fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : formData
  }).then(async (response) => {
    const text = await response.text()
    const data = text ? JSON.parse(text) : null
    if (!response.ok) {
      throw new Error(data?.detail || 'Request failed')
    }
    return data
  })
}

function Login({ onLogin }) {
  const [email, setEmail] = useState('avkc@jobpilot.local')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function submit(event) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await apiRequest('/auth/login', {
        method: 'POST',
        body: { email, password }
      })
      onLogin(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="login-shell">
      <section className="login-panel">
        <div className="brand-row">
          <Briefcase aria-hidden="true" />
          <div>
            <h1>JobPilot Pi</h1>
            <p>Local job assistant</p>
          </div>
        </div>
        <form onSubmit={submit} className="form-grid">
          <label>
            Email
            <input value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="username" />
          </label>
          <label>
            Password
            <input
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              type="password"
              autoComplete="current-password"
            />
          </label>
          {error && <div className="error">{error}</div>}
          <button className="primary-btn" disabled={loading} type="submit">
            <KeyRound size={18} />
            {loading ? 'Signing in' : 'Sign in'}
          </button>
        </form>
      </section>
    </main>
  )
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('jobpilot_token') || '')
  const [user, setUser] = useState(null)
  const [activeTab, setActiveTab] = useState('jobs')

  function handleLogin(data) {
    localStorage.setItem('jobpilot_token', data.access_token)
    setToken(data.access_token)
    setUser(data.user)
  }

  function logout() {
    localStorage.removeItem('jobpilot_token')
    setToken('')
    setUser(null)
  }

  useEffect(() => {
    if (!token) return
    apiRequest('/auth/me', { token })
      .then(setUser)
      .catch(() => logout())
  }, [token])

  if (!token) return <Login onLogin={handleLogin} />

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-row compact">
          <Briefcase aria-hidden="true" />
          <div>
            <strong>JobPilot Pi</strong>
            <span>{user?.email}</span>
          </div>
        </div>
        <nav>
          <NavButton id="jobs" activeTab={activeTab} setActiveTab={setActiveTab} icon={Search} label="Jobs" />
          <NavButton id="profile" activeTab={activeTab} setActiveTab={setActiveTab} icon={User} label="Profile" />
          <NavButton id="sources" activeTab={activeTab} setActiveTab={setActiveTab} icon={Database} label="Sources" />
          <NavButton id="assistant" activeTab={activeTab} setActiveTab={setActiveTab} icon={Wand2} label="Assistant" />
          <NavButton id="memory" activeTab={activeTab} setActiveTab={setActiveTab} icon={MessageSquare} label="Memory" />
          <NavButton id="settings" activeTab={activeTab} setActiveTab={setActiveTab} icon={Settings} label="Settings" />
        </nav>
        <button className="ghost-btn" onClick={logout}>
          <LogOut size={18} />
          Sign out
        </button>
      </aside>
      <main className="workspace">
        {activeTab === 'jobs' && <Jobs token={token} />}
        {activeTab === 'profile' && <Profile token={token} />}
        {activeTab === 'sources' && <Sources token={token} />}
        {activeTab === 'assistant' && <Assistant token={token} />}
        {activeTab === 'memory' && <Memory token={token} />}
        {activeTab === 'settings' && <SettingsView token={token} />}
      </main>
    </div>
  )
}

function NavButton({ id, activeTab, setActiveTab, icon: Icon, label }) {
  return (
    <button className={activeTab === id ? 'nav-btn active' : 'nav-btn'} onClick={() => setActiveTab(id)}>
      <Icon size={18} />
      {label}
    </button>
  )
}

function Jobs({ token }) {
  const [jobs, setJobs] = useState([])
  const [selected, setSelected] = useState(null)
  const [filters, setFilters] = useState({ min_score: 0, role: '', status: '' })
  const [error, setError] = useState('')

  async function loadJobs() {
    setError('')
    const params = new URLSearchParams()
    if (filters.min_score) params.set('min_score', filters.min_score)
    if (filters.role) params.set('role', filters.role)
    if (filters.status) params.set('status', filters.status)
    try {
      const data = await apiRequest(`/jobs?${params.toString()}`, { token })
      setJobs(data)
      setSelected(data[0] || null)
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => {
    loadJobs()
  }, [])

  return (
    <section className="view-grid two-column">
      <div className="panel">
        <ViewHeader title="Jobs" action={<IconButton icon={RefreshCw} label="Refresh" onClick={loadJobs} />} />
        <div className="filter-row">
          <input
            aria-label="Minimum score"
            type="number"
            min="0"
            max="100"
            value={filters.min_score}
            onChange={(event) => setFilters({ ...filters, min_score: event.target.value })}
          />
          <input
            aria-label="Role"
            placeholder="Role"
            value={filters.role}
            onChange={(event) => setFilters({ ...filters, role: event.target.value })}
          />
          <select
            aria-label="Status"
            value={filters.status}
            onChange={(event) => setFilters({ ...filters, status: event.target.value })}
          >
            <option value="">Any status</option>
            <option value="new">New</option>
            <option value="saved">Saved</option>
            <option value="applied">Applied</option>
            <option value="archived">Archived</option>
          </select>
          <button className="secondary-btn" onClick={loadJobs}>
            <Search size={18} />
            Filter
          </button>
        </div>
        {error && <div className="error">{error}</div>}
        <div className="job-list">
          {jobs.map((job) => (
            <button
              key={job.id}
              className={selected?.id === job.id ? 'job-card selected' : 'job-card'}
              onClick={() => setSelected(job)}
            >
              <span className="score">{job.score}</span>
              <span>
                <strong>{job.title}</strong>
                <small>{job.company || 'Unknown company'} - {job.location || 'Unknown location'}</small>
              </span>
            </button>
          ))}
          {!jobs.length && <EmptyState text="No jobs yet. Add a source and scan it." />}
        </div>
      </div>
      <JobDetail token={token} job={selected} />
    </section>
  )
}

function JobDetail({ token, job }) {
  const [status, setStatus] = useState(job?.status || 'new')
  const [message, setMessage] = useState('')

  useEffect(() => {
    setStatus(job?.status || 'new')
    setMessage('')
  }, [job])

  if (!job) return <div className="panel"><EmptyState text="Select a job." /></div>

  async function saveStatus() {
    const updated = await apiRequest(`/jobs/${job.id}/status`, {
      token,
      method: 'PATCH',
      body: { status }
    })
    setMessage(`Saved as ${updated.status}`)
  }

  async function createApplication() {
    await apiRequest('/applications', { token, method: 'POST', body: { job_id: job.id } })
    setMessage('Application draft created')
  }

  return (
    <div className="panel detail-panel">
      <ViewHeader
        title={job.title}
        action={
          <a className="secondary-link" href={job.url} target="_blank" rel="noreferrer">
            Open
          </a>
        }
      />
      <div className="meta-row">
        <span>{job.company || 'Unknown company'}</span>
        <span>{job.location || 'Unknown location'}</span>
        <span>{job.remote ? 'Remote' : 'On-site or hybrid'}</span>
      </div>
      <div className="score-band">
        <strong>{job.score}</strong>
        <span>{job.match_explanation}</span>
      </div>
      <p>{job.description}</p>
      <TagRow items={job.required_skills} />
      {!!job.missing_skills.length && <TagRow tone="warning" items={job.missing_skills} />}
      <div className="toolbar">
        <select value={status} onChange={(event) => setStatus(event.target.value)}>
          <option value="new">New</option>
          <option value="saved">Saved</option>
          <option value="applied">Applied</option>
          <option value="archived">Archived</option>
        </select>
        <button className="secondary-btn" onClick={saveStatus}>
          <Save size={18} />
          Save
        </button>
        <button className="primary-btn" onClick={createApplication}>
          <ClipboardList size={18} />
          Draft
        </button>
      </div>
      {message && <div className="success">{message}</div>}
    </div>
  )
}

function Profile({ token }) {
  const [profile, setProfile] = useState(null)
  const [skills, setSkills] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    apiRequest('/profile', { token }).then((data) => {
      setProfile(data)
      setSkills(data.skills.join(', '))
    })
  }, [token])

  if (!profile) return <div className="panel"><EmptyState text="Loading profile." /></div>

  async function saveProfile(event) {
    event.preventDefault()
    const data = await apiRequest('/profile', {
      token,
      method: 'PUT',
      body: {
        ...profile,
        skills: skills.split(',').map((skill) => skill.trim()).filter(Boolean)
      }
    })
    setProfile(data)
    setSkills(data.skills.join(', '))
    setMessage('Profile saved')
  }

  async function uploadResume(event) {
    const file = event.target.files?.[0]
    if (!file) return
    const formData = new FormData()
    formData.append('resume', file)
    const data = await apiRequest('/profile/resume', { token, method: 'POST', formData })
    setMessage(`Resume uploaded: ${data.filename}`)
  }

  return (
    <section className="panel narrow-panel">
      <ViewHeader title="Profile" />
      <form onSubmit={saveProfile} className="form-grid">
        <label>Full name<input value={profile.full_name || ''} onChange={(event) => setProfile({ ...profile, full_name: event.target.value })} /></label>
        <label>Target role<input value={profile.target_role || ''} onChange={(event) => setProfile({ ...profile, target_role: event.target.value })} /></label>
        <label>Location<input value={profile.location || ''} onChange={(event) => setProfile({ ...profile, location: event.target.value })} /></label>
        <label>Experience years<input type="number" min="0" value={profile.experience_years} onChange={(event) => setProfile({ ...profile, experience_years: Number(event.target.value) })} /></label>
        <label className="full-span">Skills<input value={skills} onChange={(event) => setSkills(event.target.value)} /></label>
        <label className="full-span">Resume<input type="file" accept=".pdf,.doc,.docx,.txt" onChange={uploadResume} /></label>
        <button className="primary-btn" type="submit"><Save size={18} />Save profile</button>
      </form>
      {message && <div className="success">{message}</div>}
    </section>
  )
}

function Sources({ token }) {
  const [sources, setSources] = useState([])
  const [form, setForm] = useState({ name: '', url: '', source_type: 'mock', enabled: true, scan_interval_minutes: 5 })
  const [message, setMessage] = useState('')

  async function loadSources() {
    setSources(await apiRequest('/sources', { token }))
  }

  useEffect(() => {
    loadSources()
  }, [])

  async function addSource(event) {
    event.preventDefault()
    await apiRequest('/sources', { token, method: 'POST', body: form })
    setForm({ name: '', url: '', source_type: 'mock', enabled: true, scan_interval_minutes: 5 })
    await loadSources()
  }

  async function scan(id) {
    const result = await apiRequest(`/sources/${id}/scan`, { token, method: 'POST' })
    setMessage(`Scan found ${result.discovered}; created ${result.created}, updated ${result.updated}`)
  }

  return (
    <section className="view-grid two-column">
      <div className="panel">
        <ViewHeader title="Sources" />
        <form onSubmit={addSource} className="form-grid">
          <label>Name<input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} /></label>
          <label>URL<input value={form.url} onChange={(event) => setForm({ ...form, url: event.target.value })} /></label>
          <label>Interval<input type="number" min="5" value={form.scan_interval_minutes} onChange={(event) => setForm({ ...form, scan_interval_minutes: Number(event.target.value) })} /></label>
          <label className="check-row"><input type="checkbox" checked={form.enabled} onChange={(event) => setForm({ ...form, enabled: event.target.checked })} />Enabled</label>
          <button className="primary-btn" type="submit"><Plus size={18} />Add source</button>
        </form>
        {message && <div className="success">{message}</div>}
      </div>
      <div className="panel">
        <ViewHeader title="Configured" action={<IconButton icon={RefreshCw} label="Refresh" onClick={loadSources} />} />
        <div className="stack-list">
          {sources.map((source) => (
            <div className="source-row" key={source.id}>
              <span>
                <strong>{source.name}</strong>
                <small>{source.url}</small>
              </span>
              <button className="secondary-btn" onClick={() => scan(source.id)}><RefreshCw size={18} />Scan</button>
            </div>
          ))}
          {!sources.length && <EmptyState text="No sources configured." />}
        </div>
      </div>
    </section>
  )
}

function Assistant({ token }) {
  const [jobs, setJobs] = useState([])
  const [jobId, setJobId] = useState('')
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)

  useEffect(() => {
    apiRequest('/jobs', { token }).then(setJobs)
  }, [token])

  async function generate() {
    if (!jobId) return
    const data = await apiRequest('/applications/assistant', {
      token,
      method: 'POST',
      body: { job_id: Number(jobId), question }
    })
    setResult(data)
  }

  return (
    <section className="view-grid two-column">
      <div className="panel">
        <ViewHeader title="Assistant" />
        <div className="form-grid">
          <label className="full-span">Job<select value={jobId} onChange={(event) => setJobId(event.target.value)}>
            <option value="">Select job</option>
            {jobs.map((job) => <option key={job.id} value={job.id}>{job.title} - {job.company}</option>)}
          </select></label>
          <label className="full-span">Question<textarea value={question} onChange={(event) => setQuestion(event.target.value)} rows="5" /></label>
          <button className="primary-btn" onClick={generate}><Wand2 size={18} />Generate</button>
        </div>
      </div>
      <div className="panel">
        <ViewHeader title="Drafts" />
        {result ? (
          <div className="draft-grid">
            <Draft title="Cover letter" text={result.cover_letter} />
            <Draft title="Resume suggestions" text={result.resume_suggestions} />
            <Draft title="Answer draft" text={result.answer_draft} />
          </div>
        ) : <EmptyState text="Generate a draft from a selected job." />}
      </div>
    </section>
  )
}

function Memory({ token }) {
  const [items, setItems] = useState([])
  const [form, setForm] = useState({ question: '', answer: '', tags: '' })

  async function loadItems() {
    setItems(await apiRequest('/qa-memory', { token }))
  }

  useEffect(() => {
    loadItems()
  }, [])

  async function addItem(event) {
    event.preventDefault()
    await apiRequest('/qa-memory', {
      token,
      method: 'POST',
      body: {
        question: form.question,
        answer: form.answer,
        tags: form.tags.split(',').map((tag) => tag.trim()).filter(Boolean)
      }
    })
    setForm({ question: '', answer: '', tags: '' })
    await loadItems()
  }

  return (
    <section className="view-grid two-column">
      <div className="panel">
        <ViewHeader title="Q&A Memory" />
        <form onSubmit={addItem} className="form-grid">
          <label className="full-span">Question<input value={form.question} onChange={(event) => setForm({ ...form, question: event.target.value })} /></label>
          <label className="full-span">Answer<textarea value={form.answer} onChange={(event) => setForm({ ...form, answer: event.target.value })} rows="5" /></label>
          <label className="full-span">Tags<input value={form.tags} onChange={(event) => setForm({ ...form, tags: event.target.value })} /></label>
          <button className="primary-btn" type="submit"><Plus size={18} />Add memory</button>
        </form>
      </div>
      <div className="panel">
        <ViewHeader title="Saved" />
        <div className="stack-list">
          {items.map((item) => (
            <article className="memory-row" key={item.id}>
              <strong>{item.question}</strong>
              <p>{item.answer}</p>
              <TagRow items={item.tags} />
            </article>
          ))}
          {!items.length && <EmptyState text="No saved answers yet." />}
        </div>
      </div>
    </section>
  )
}

function SettingsView({ token }) {
  const [settings, setSettings] = useState(null)

  useEffect(() => {
    apiRequest('/settings', { token }).then(setSettings)
  }, [token])

  if (!settings) return <div className="panel"><EmptyState text="Loading settings." /></div>

  return (
    <section className="panel narrow-panel">
      <ViewHeader title="Settings" />
      <div className="settings-grid">
        <Setting label="Environment" value={settings.environment} />
        <Setting label="AI provider" value={settings.ai_provider} />
        <Setting label="AI model" value={settings.ai_model} />
        <Setting label="OpenAI key" value={settings.openai_configured ? 'Configured' : 'Not configured'} />
        <Setting label="Default scan" value={`${settings.default_scan_interval_minutes} minutes`} />
        <Setting label="Upload limit" value={`${settings.max_upload_mb} MB`} />
      </div>
    </section>
  )
}

function ViewHeader({ title, action }) {
  return (
    <div className="view-header">
      <h2>{title}</h2>
      {action}
    </div>
  )
}

function IconButton({ icon: Icon, label, onClick }) {
  return (
    <button className="icon-btn" onClick={onClick} title={label} aria-label={label}>
      <Icon size={18} />
    </button>
  )
}

function TagRow({ items, tone = 'default' }) {
  if (!items?.length) return null
  return (
    <div className="tag-row">
      {items.map((item) => <span className={`tag ${tone}`} key={item}>{item}</span>)}
    </div>
  )
}

function Draft({ title, text }) {
  return (
    <article className="draft">
      <h3>{title}</h3>
      <pre>{text}</pre>
    </article>
  )
}

function EmptyState({ text }) {
  return <div className="empty-state">{text}</div>
}

function Setting({ label, value }) {
  return (
    <div className="setting-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
