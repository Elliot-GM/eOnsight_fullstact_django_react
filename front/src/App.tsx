import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Header';
import BridgeList from './components/BridgesList';
import Chart from './components/Chart';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import fetchBridges from './tools/fetchBridges';
import Bridge from './models/bridge';
import { useEffect, useState } from 'react';
import BridgeForm from './components/BridgeForm';

const App: React.FC = () => {
  const [bridges, setBridges] = useState<Bridge[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadBridges = async () => {
      try {
        const data = await fetchBridges();
        setBridges(data);
      } catch (error) {
        setError('Error loading bridges');
      } finally {
        setLoading(false);
      }
    };

    loadBridges();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  
  return (
    <div>
      <Header />
      <Router>
        <Routes>
          <Route path="/" element={<BridgeList bridges={bridges} setBridges={setBridges} />} />
          <Route path="/charts" element={<Chart bridges={bridges} />} />
          <Route path="/add-bridge" element={<BridgeForm />} />
          <Route path="/bridge/:id" element={<BridgeForm/>} />
        </Routes>
      </Router>
    </div>
  );
};
    
export default App;