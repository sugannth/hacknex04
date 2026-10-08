import { useRef, useState } from "react";
import "./App.css";

function App() {
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [processed, setProcessed] = useState(false);
  const [activeNav, setActiveNav] = useState("Workspace");
  const [copied, setCopied] = useState(false);

  const [text, setText] = useState(
    "Your digitized handwriting will appear here after processing."
  );

  const processDemo = () => {
    if (!file) return;

    setProcessing(true);
    setProcessed(false);

    setTimeout(() => {
      setProcessing(false);
      setProcessed(true);

      setText(
        "The patient has fever and cough for three days. Please continue medication and return for a follow-up consultation."
      );
    }, 2200);
  };

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    if (!selectedFile.type.startsWith("image/")) {
      alert("Please select an image file.");
      return;
    }

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setProcessed(false);
    setText("Ready for digitization.");
  };

  const handleInputChange = (e) => {
    handleFile(e.target.files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
  };

  const clearFile = () => {
    setFile(null);
    setPreview(null);
    setProcessed(false);
    setProcessing(false);
    setText("Your digitized handwriting will appear here after processing.");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const copyText = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 1500);
  };

  const downloadText = () => {
    const blob = new Blob([text], {
      type: "text/plain",
    });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "digitized-handwriting.txt";
    a.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div className="app-shell">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-mark">H</div>

          <div>
            <div className="brand-name">HandwritingAI</div>
            <div className="brand-version">DIGITIZATION ENGINE</div>
          </div>
        </div>

        <div className="sidebar-section">
          <div className="section-label">WORKSPACE</div>

          {[
            ["⌂", "Workspace"],
            ["◈", "History"],
            ["▣", "Samples"],
          ].map(([icon, name]) => (
            <button
              key={name}
              className={`nav-item ${
                activeNav === name ? "active" : ""
              }`}
              onClick={() => setActiveNav(name)}
            >
              <span>{icon}</span>
              {name}
            </button>
          ))}
        </div>

        <div className="sidebar-section">
          <div className="section-label">SYSTEM</div>

          <button className="nav-item">
            <span>⚙</span>
            Settings
          </button>

          <button className="nav-item">
            <span>?</span>
            Documentation
          </button>
        </div>

        <div className="sidebar-bottom">

          <div className="system-card">
            <div className="online-dot"></div>

            <div>
              <strong>AI Engine Online</strong>
              <small>Ready to process</small>
            </div>
          </div>

          <div className="profile">
            <div className="avatar">P3</div>

            <div>
              <strong>Person 3</strong>
              <small>Frontend Engineer</small>
            </div>
          </div>

        </div>

      </aside>


      {/* MAIN AREA */}
      <main className="main-area">

        {/* TOPBAR */}
        <header className="topbar">

          <div>
            <div className="breadcrumb">
              PROJECT / WORKSPACE
            </div>

            <h1>Extreme Handwriting Digitization</h1>
          </div>

          <div className="top-actions">

            <div className="status-pill">
              <span></span>
              System operational
            </div>

            <button className="icon-button">
              ◐
            </button>

            <div className="top-avatar">
              P3
            </div>

          </div>

        </header>


        {/* CONTENT */}
        <div className="content">

          {/* HERO */}
          <section className="hero">

            <div className="hero-copy">

              <div className="eyebrow">
                AI-POWERED HANDWRITING RECOGNITION
              </div>

              <h2>
                Turn impossible handwriting
                <br />
                into <span>clean digital text.</span>
              </h2>

              <p>
                Designed for cramped notes, inconsistent handwriting,
                crossed-out words, margin annotations and real-world
                messy documents.
              </p>

            </div>

            <div className="hero-stats">

              <div>
                <strong>94%</strong>
                <span>Recognition target</span>
              </div>

              <div>
                <strong>3</strong>
                <span>AI stages</span>
              </div>

              <div>
                <strong>∞</strong>
                <span>Editable output</span>
              </div>

            </div>

          </section>


          {/* UPLOAD WORKSPACE */}
          <section className="workspace-grid">

            {/* LEFT */}
            <div className="panel upload-panel">

              <div className="panel-heading">

                <div>
                  <span className="panel-kicker">
                    STEP 01
                  </span>

                  <h3>Upload document</h3>
                </div>

                {file && (
                  <button
                    className="text-button danger"
                    onClick={clearFile}
                  >
                    Clear
                  </button>
                )}

              </div>


              {!file ? (

                <div
                  className={`drop-zone ${
                    dragging ? "dragging" : ""
                  }`}
                  onDragOver={(e) => {
                    e.preventDefault();
                    setDragging(true);
                  }}
                  onDragLeave={() => setDragging(false)}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current.click()}
                >

                  <div className="drop-icon">
                    ↑
                  </div>

                  <h4>
                    Drop your handwriting here
                  </h4>

                  <p>
                    Drag an image into this area or browse
                    from your device.
                  </p>

                  <button
                    className="primary-button"
                    onClick={(e) => {
                      e.stopPropagation();
                      fileInputRef.current.click();
                    }}
                  >
                    Upload document
                    <span>→</span>
                  </button>

                  <div className="format-info">
                    PNG · JPG · JPEG · MAX 20MB
                  </div>

                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleInputChange}
                    hidden
                  />

                </div>

              ) : (

                <div className="uploaded-state">

                  <div className="file-row">

                    <div className="file-icon">
                      IMG
                    </div>

                    <div className="file-details">
                      <strong>{file.name}</strong>

                      <span>
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                        {" · "}
                        Image ready
                      </span>
                    </div>

                    <button
                      className="small-button"
                      onClick={() =>
                        fileInputRef.current.click()
                      }
                    >
                      Replace
                    </button>

                  </div>

                  <div className="image-preview-wrapper">

                    <img
                      src={preview}
                      alt="Handwritten document"
                    />

                    <div className="image-overlay">
                      <span>ORIGINAL DOCUMENT</span>
                    </div>

                  </div>

                </div>

              )}

            </div>


            {/* RIGHT */}
            <div className="panel pipeline-panel">

              <div className="panel-heading">

                <div>
                  <span className="panel-kicker">
                    STEP 02
                  </span>

                  <h3>Recognition pipeline</h3>
                </div>

                <span className="live-badge">
                  LIVE
                </span>

              </div>

              <div className="pipeline">

                <PipelineStep
                  number="01"
                  title="Image preprocessing"
                  description="Normalize, enhance and isolate writing"
                  state={
                    processing
                      ? "processing"
                      : processed
                      ? "complete"
                      : "waiting"
                  }
                />

                <PipelineLine />

                <PipelineStep
                  number="02"
                  title="Handwriting recognition"
                  description="Extract characters, words and layout"
                  state={
                    processing
                      ? "processing"
                      : processed
                      ? "complete"
                      : "waiting"
                  }
                />

                <PipelineLine />

                <PipelineStep
                  number="03"
                  title="AI contextual correction"
                  description="Resolve ambiguous recognition results"
                  state={
                    processing
                      ? "processing"
                      : processed
                      ? "complete"
                      : "waiting"
                  }
                />

              </div>

              <button
                className="process-button"
                disabled={!file || processing}
                onClick={processDemo}
              >
                {processing ? (
                  <>
                    <span className="spinner"></span>
                    Processing document...
                  </>
                ) : (
                  <>
                    ✦ Digitize handwriting
                    <span>→</span>
                  </>
                )}
              </button>

            </div>

          </section>


          {/* RESULTS */}
          <section className="results-section">

            <div className="section-title-row">

              <div>
                <span className="panel-kicker">
                  STEP 03
                </span>

                <h3>Digitization result</h3>
              </div>

              {processed && (
                <div className="success-badge">
                  ✓ PROCESSING COMPLETE
                </div>
              )}

            </div>


            <div className="results-grid">

              {/* TEXT */}
              <div className="panel text-panel">

                <div className="result-header">

                  <div>
                    <span className="result-label">
                      EDITABLE TRANSCRIPTION
                    </span>

                    <h4>Clean digital text</h4>
                  </div>

                  <div className="result-actions">

                    <button onClick={copyText}>
                      {copied ? "✓ Copied" : "Copy"}
                    </button>

                    <button onClick={downloadText}>
                      Download
                    </button>

                  </div>

                </div>

                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  className="result-editor"
                />

              </div>


              {/* ANALYTICS */}
              <div className="panel analytics-panel">

                <div className="result-label">
                  AI ANALYSIS
                </div>

                <h4>Recognition quality</h4>

                <div className="confidence">

                  <div className="confidence-circle">
                    <strong>
                      {processed ? "94" : "--"}
                    </strong>

                    <span>%</span>
                  </div>

                  <div>
                    <strong>Confidence score</strong>

                    <p>
                      {processed
                        ? "High confidence recognition"
                        : "Process a document to calculate"}
                    </p>
                  </div>

                </div>


                <div className="metric-grid">

                  <Metric
                    value={processed ? "42" : "--"}
                    label="Words"
                  />

                  <Metric
                    value={processed ? "06" : "--"}
                    label="Corrections"
                  />

                  <Metric
                    value={processed ? "02" : "--"}
                    label="Uncertain"
                  />

                  <Metric
                    value={processed ? "98%" : "--"}
                    label="Layout"
                  />

                </div>

              </div>

            </div>

          </section>


          {/* CORRECTIONS */}
          <section className="panel corrections-panel">

            <div className="section-title-row">

              <div>
                <span className="panel-kicker">
                  AI INSIGHTS
                </span>

                <h3>Recognition corrections</h3>
              </div>

              <span className="muted">
                Context-aware correction
              </span>

            </div>

            <div className="corrections-table">

              <div className="table-head">
                <span>RECOGNIZED</span>
                <span>CORRECTED</span>
                <span>CONFIDENCE</span>
              </div>

              <Correction
                original="patlent"
                corrected="patient"
                confidence="96%"
              />

              <Correction
                original="recieve"
                corrected="receive"
                confidence="93%"
              />

              <Correction
                original="nd"
                corrected="and"
                confidence="91%"
              />

            </div>

          </section>


          {/* FOOTER */}
          <footer>

            <span>
              HandwritingAI · Extreme Bad-Handwriting Digitization
            </span>

            <span>
              Person 3 · Frontend
            </span>

          </footer>

        </div>

      </main>

    </div>
  );
}


/* PIPELINE COMPONENT */

function PipelineStep({
  number,
  title,
  description,
  state,
}) {
  return (
    <div className={`pipeline-step ${state}`}>

      <div className="pipeline-number">
        {state === "complete" ? "✓" : number}
      </div>

      <div className="pipeline-content">
        <strong>{title}</strong>
        <span>{description}</span>
      </div>

      <div className="pipeline-status">
        {state === "processing"
          ? "RUNNING"
          : state === "complete"
          ? "DONE"
          : "WAITING"}
      </div>

    </div>
  );
}


/* PIPELINE LINE */

function PipelineLine() {
  return <div className="pipeline-line"></div>;
}


/* METRIC */

function Metric({ value, label }) {
  return (
    <div className="metric">

      <strong>{value}</strong>

      <span>{label}</span>

    </div>
  );
}


/* CORRECTION */

function Correction({
  original,
  corrected,
  confidence,
}) {
  return (
    <div className="table-row">

      <span className="wrong">
        {original}
      </span>

      <span className="arrow">
        →
      </span>

      <span className="correct">
        {corrected}
      </span>

      <span className="confidence-text">
        {confidence}
      </span>

    </div>
  );
}

export default App;