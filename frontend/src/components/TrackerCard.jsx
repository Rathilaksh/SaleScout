import { useNavigate } from 'react-router-dom'
import { trackerApi } from '../api/endpoints'
import { formatPrice, formatDate } from '../utils/helpers'

export default function TrackerCard({ tracker, onDelete }) {
  const navigate = useNavigate()

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this tracker?')) {
      try {
        await trackerApi.delete(tracker.id)
        onDelete(tracker.id)
      } catch (err) {
        alert('Failed to delete tracker')
      }
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg hover:shadow-xl transition overflow-hidden">
      {tracker.image_url && (
        <img
          src={tracker.image_url}
          alt={tracker.product_title}
          className="w-full h-48 object-cover"
        />
      )}
      <div className="p-4">
        <h3
          onClick={() => navigate(`/trackers/${tracker.id}`)}
          className="text-lg font-bold text-gray-800 hover:text-blue-600 cursor-pointer mb-2"
        >
          {tracker.product_title}
        </h3>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-gray-600 text-sm">Current Price</p>
            <p className="text-xl font-bold text-gray-800">
              {tracker.last_price ? formatPrice(tracker.last_price) : 'N/A'}
            </p>
          </div>
          <div>
            <p className="text-gray-600 text-sm">Target Price</p>
            <p className="text-xl font-bold text-green-600">{formatPrice(tracker.target_price)}</p>
          </div>
        </div>

        {tracker.last_checked_at && (
          <p className="text-gray-600 text-xs mb-4">
            Last checked: {formatDate(tracker.last_checked_at)}
          </p>
        )}

        <div className="flex gap-2">
          <button
            onClick={() => navigate(`/trackers/${tracker.id}`)}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-lg transition text-sm"
          >
            View Details
          </button>
          <button
            onClick={handleDelete}
            className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition text-sm"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  )
}
