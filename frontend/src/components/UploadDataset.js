import axios from "axios";
import { useState } from "react";

export default function UploadDataset() {
  const [file, setFile] = useState(null);
  const API = process.env.REACT_APP_API_URL;

  const upload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API}/upload`, formData);
    alert("Uploaded successfully: " + res.data.filename);
  };

  return (
    <div>
      <h2>Upload CSV</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={upload}>Upload</button>
    </div>
  );
}
