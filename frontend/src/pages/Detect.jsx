export default function Detect() {
  return (
    <div style={{ padding: 20 }}>
      <h2>Live Face Recognition</h2>
      <p>Make sure Python face_service.py is running.</p>
      <img
        src="http://localhost:5000/video"
        alt="Live video"
        style={{ width: 600 }}
      />
    </div>
  );
}
