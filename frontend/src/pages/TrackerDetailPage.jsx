import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { trackerApi } from '../api/endpoints'
import { formatPrice, formatDate } from '../utils/helpers'

export default function TrackerDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [tracker, setTracker] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editing, setEditing] = useState(false)
  const [targetPrice, setTargetPrice] = useState('')
  const [pollingInterval, setPollingInterval] = useState('')

  useEffect(() => {
    fetchTracker()
  }, [id])

  const fetchTracker = async () => {
    try {
      setLoading(true)
      const response = await trackerApi.getById(parseInt(id))
      setTracker(response.data)
      setTargetPrice(response.data.target_price)
      setPollingInterval(response.data.polling_interval_minutes)
    } catch (err) {
      setError('Failed to load tracker')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdate = async () => {
    try {
      const response = await trackerApi.update(parseInt(id), {
        target_price: parseFloat(targetPrice),
        polling_interval_minutes: parseInt(pollingInterval),
      })
      setTracker(response.data)
      setEditing(false)
    } catch (err) {
      setError('Failed to update tracker')
    }
  }

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this tracker?')) {
      try {
        await trackerApi.delete(parseInt(id))
        navigate('/dashboard')
      } catch (err) {
        setError('Failed to delete tracker')
      }
    }
  }

  if (loading) return <div className="p-8 text-center">Loading...</div>
  if (!tracker) return <div className="p-8 text-center">Tracker not found</div>

  const chartData = tracker.price_history
    ?.map((h) => ({
      date: new Date(h.checked_at).toLocaleDateString('en-IN'),
      price: h.price,
    }))
    .reverse() || []

  return (
    <div className="p-8">
      <button
        onClick={() => navigate('/dashboard')}
        className="text-blue-600 hover:text-blue-800 mb-4"
      >
        ← Back to Dashboard
      </button>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div className="flex items-start gap-6">
          {tracker.image_url && (
            <img
              src={tracker.image_url}
              alt={tracker.product_title}
              className="w-32 h-32 object-cover rounded-lg"
            />
          )}
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">{tracker.product_title}</h1>
            <a
              href={tracker.product_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 mb-4 block"
            >
              View Product →
            </a>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-gray-600">Current Price</p>
                <p className="text-2xl font-bold text-gray-800">
                  {tracker.last_price ? formatPrice(tracker.last_price) : 'Not available'}
                </p>
              </div>
              <div>
                <p className="text-gray-600">Target Price</p>
                <p className="text-2xl font-bold text-green-600">{formatPrice(tracker.target_price)}</p>
              </div>
            </div>
            <p className="text-gray-600 mt-4">
              Last checked: {tracker.last_checked_at ? formatDate(tracker.last_checked_at) : 'Never'}
            </p>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t">
          {!editing ? (
            <div className="flex gap-4">
              <button
                onClick={() => setEditing(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition"
              >
                Edit Settings
              </button>
              <button
                onClick={handleDelete}
                className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-lg transition"
              >
                Delete Tracker
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <label className="block text-gray-700 font-medium mb-2">Target Price</label>
                <input
                  type="number"
                  value={targetPrice}
                  onChange={(e) => setTargetPrice(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-medium mb-2">Polling Interval (minutes)</label>
                <input
                  type="number"
                  value={pollingInterval}
                  onChange={(e) => setPollingInterval(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  min="5"
                  max="1440"
                />
              </div>
              <div className="flex gap-4">
                <button
                  onClick={handleUpdate}
                  className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg transition"
                >
                  Save
                </button>
                <button
                  onClick={() => setEditing(false)}
                  className="bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-6 rounded-lg transition"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {chartData.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Price History</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip formatter={(value) => formatPrice(value)} />
              <Line type="monotone" dataKey="price" stroke="#3B82F6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
