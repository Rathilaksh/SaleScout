import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { trackerApi } from '../api/endpoints'
import TrackerCard from '../components/TrackerCard'
import AddTrackerModal from '../components/AddTrackerModal'

export default function DashboardPage() {
  const { user } = useAuth()
  const [trackers, setTrackers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    fetchTrackers()
  }, [])

  const fetchTrackers = async () => {
    try {
      setLoading(true)
      const response = await trackerApi.getAll()
      setTrackers(response.data)
    } catch (err) {
      setError('Failed to load trackers')
    } finally {
      setLoading(false)
    }
  }

  const handleTrackerAdded = (newTracker) => {
    setTrackers([...trackers, newTracker])
    setShowModal(false)
  }

  const handleTrackerDeleted = (id) => {
    setTrackers(trackers.filter((t) => t.id !== id))
  }

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
          <p className="text-gray-600">Welcome, {user?.email}</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition"
        >
          + Add Tracker
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Loading trackers...</p>
        </div>
      ) : trackers.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">No trackers yet</p>
          <button
            onClick={() => setShowModal(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition"
          >
            Start tracking a product
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trackers.map((tracker) => (
            <TrackerCard
              key={tracker.id}
              tracker={tracker}
              onDelete={handleTrackerDeleted}
            />
          ))}
        </div>
      )}

      {showModal && (
        <AddTrackerModal
          onClose={() => setShowModal(false)}
          onTrackerAdded={handleTrackerAdded}
        />
      )}
    </div>
  )
}
