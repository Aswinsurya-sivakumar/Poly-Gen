
import ModelViewer from "./ModelViewer";
import "./App.css";

function App() {
  return (
    <div className="app">
      <h1>PolyGen</h1>

      <p>Generative Text-to-3D Asset Pipeline</p>

      <h2>3D Model Viewer</h2>

      <ModelViewer />

      <p className="instructions">
        Left Click: Rotate | Scroll: Zoom | Right Click: Pan
      </p>
    </div>
  );
}

export default App;
