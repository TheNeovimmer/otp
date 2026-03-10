import { useState } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'
import './Auth.css'

const API_URL = 'http://localhost:8000'

function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [otp, setOtp] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [step, setStep] = useState(1)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleRequestOTP = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await axios.post(`${API_URL}/otp/request`, { email })
      setSuccess('OTP sent to your email!')
      setStep(2)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send OTP')
    }
  }

  const handleVerifyOTP = async (e) => {
    e.preventDefault()
    setError('')

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    try {
      await axios.post(`${API_URL}/otp/verify`, {
        email,
        code: otp,
        new_password: newPassword
      })
      setSuccess('Password reset successful!')
      setTimeout(() => window.location.href = '/login', 2000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid OTP')
    }
  }

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={step === 1 ? handleRequestOTP : handleVerifyOTP}>
        <h2>Reset Password</h2>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        
        {step === 1 ? (
          <>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <button type="submit">Send OTP</button>
          </>
        ) : (
          <>
            <input
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="New Password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Confirm New Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
            <button type="submit">Reset Password</button>
          </>
        )}
        <p>
          <Link to="/login">Back to Login</Link>
        </p>
      </form>
    </div>
  )
}

export default ForgotPassword
