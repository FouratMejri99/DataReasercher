import axios from "axios";
import { useEffect, useState } from "react";

export default function Stats() {
  const [stats, setStats] = useState(null);
  const API = process.env.REACT_APP_API_URL;

  useEffect(() => {
    axios.get(`${API}/stats`).then((res) => setStats(res.data));
  }, []);

  if (!stats) return <p>Loading...</p>;

  return (
    <div>
      <h2>Dataset Statistics</h2>
      <pre>{JSON.stringify(stats, null, 2)}</pre>
    </div>
  );
}
