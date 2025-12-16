# SaleScout Frontend

## Structure
```
frontend/
  src/
    api/              # API client & endpoints
      axios.js        # Axios instance with interceptors
      endpoints.js    # API wrapper functions
    components/       # Reusable components
      Layout.jsx
      TrackerCard.jsx
      AddTrackerModal.jsx
    pages/            # Route pages
      LoginPage.jsx
      RegisterPage.jsx
      DashboardPage.jsx
      TrackerDetailPage.jsx
    context/          # React Context
      AuthContext.jsx # Auth state management
    utils/            # Helper functions
      helpers.js      # Formatting utilities
    App.jsx           # Main app component
    main.jsx          # Entry point
    index.css         # Global styles
```

## Running Locally
```bash
npm install
npm run dev
```

## Environment Variables
Create `.env.local` if needed:
```
VITE_API_URL=http://localhost:8000
```

## Building for Production
```bash
npm run build
npm run preview  # Preview production build
```
