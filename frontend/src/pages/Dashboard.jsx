import { useEffect, useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import './Auth.css'

const API_URL = 'http://localhost:8000'

function Dashboard() {
  const [user, setUser] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('access_token')
      if (!token) {
        navigate('/login')
        return
      }
      try {
        const res = await axios.get(`${API_URL}/users/me`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        setUser(res.data)
      } catch (err) {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          try {
            const res = await axios.post(`${API_URL}/auth/refresh`, {
              refresh_token: refreshToken
            })
            localStorage.setItem('access_token', res.data.access_token)
            localStorage.setItem('refresh_token', res.data.refresh_token)
            const retry = await axios.get(`${API_URL}/users/me`, {
              headers: { Authorization: `Bearer ${res.data.access_token}` }
            })
            setUser(retry.data)
          } catch {
            navigate('/login')
          }
        } else {
          navigate('/login')
        }
      }
    }
    fetchUser()
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }

  if (!user) return <div className="auth-container">Loading...</div>

  return (
    <div className="auth-container">
      <div className="dashboard">
        <h2>Welcome!</h2>
        <div className="user-info">
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>ID:</strong> {user.id}</p>
          <p><strong>Active:</strong> {user.is_active ? 'Yes' : 'No'}</p>
          <p><strong>Created:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
        </div>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </div>
    </div>
  )
}

export default Dashboard
