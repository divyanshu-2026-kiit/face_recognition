import { useEffect, useRef, useState } from "react";
import axios from "axios";

const API = "http://localhost:4000";

export default function Train() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [name, setName] = useState("");
  const [count, setCount] = useState(0);
  const target = 50; // number of images to capture
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    (async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      await videoRef.current.play();
    })();
  }, []);

  const capture = async () => {
    if (!name) return alert("Enter a name");
    setBusy(true);
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");

    for (let i = count; i < target; i++) {
      ctx.drawImage(video, 0, 0);
      const imageBase64 = canvas.toDataURL("image/jpeg");
      await axios.post(`${API}/api/samples/capture`, { name, imageBase64 });
      setCount(i + 1);
      await new Promise((r) => setTimeout(r, 120));
    }

    // trigger python training
    const res = await axios.post(`${API}/api/train`);
    if (res.data.ok) alert("Training successful");
    else alert("Training failed");

    setBusy(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Train Model</h2>
      <input
        placeholder="Enter person name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <div>
        <video ref={videoRef} style={{ width: 480 }} />
        <canvas ref={canvasRef} style={{ display: "none" }} />
      </div>
      <button onClick={capture} disabled={busy}>
        {busy
          ? `Capturing… ${count}/${target}`
          : `Start Capture & Train (${count}/${target})`}
      </button>
    </div>
  );
}
