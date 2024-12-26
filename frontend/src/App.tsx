import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from '@/components/HomePage';
import RedirectPage from '@/components/RedirectPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/:shortCode" element={<RedirectPage />} />
      </Routes>
    </Router>
  );
}

export default App;
