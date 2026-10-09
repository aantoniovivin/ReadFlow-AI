import { useRef, useState } from 'react'
import { FileUp, LoaderCircle, Sparkles } from 'lucide-react'

export default function FileUpload({ onUpload, busy, progress = 0, phase = 'uploading' }) {
  const input = useRef(null)
  const [dragging, setDragging] = useState(false)
  const select = (file) => { if (file) onUpload(file) }
  return <main className="welcome-wrap">
    <div className="welcome-card" onDragOver={e => {e.preventDefault();setDragging(true)}} onDragLeave={() => setDragging(false)} onDrop={e => {e.preventDefault();setDragging(false);select(e.dataTransfer.files[0])}}>
      <div className="welcome-orb"><Sparkles size={25}/></div>
      <p className="eyebrow">YOUR DOCUMENT, MADE CLEAR</p>
      <h1>Read less.<br/><span>Understand more.</span></h1>
      <p className="welcome-copy">Turn dense documents and PDFs into a clear, structured briefing. Keep every definition connected to its source.</p>
      <button className={`dropzone ${dragging ? 'is-dragging' : ''} ${busy ? 'is-busy' : ''}`} onClick={() => input.current?.click()} disabled={busy}>
        {busy ? <LoaderCircle className="spin"/> : <FileUp/>}
        <strong>{busy ? (phase === 'processing' ? 'Building your briefing…' : 'Uploading your document…') : 'Drop a PDF or Word document (.docx) here'}</strong>
        {busy ? <div className="upload-progress-wrap">
          <div className="upload-progress-meta"><span>{phase === 'processing' ? 'Summarizing key pages' : 'Uploading document'}</span><strong>{phase === 'processing' ? 'Working…' : `${progress}%`}</strong></div>
          <div className="upload-progress-track" role="progressbar" aria-label={phase === 'processing' ? 'Preparing document' : 'Uploading document'} aria-valuemin="0" aria-valuemax="100" aria-valuenow={progress}>
            <span className={phase === 'processing' ? 'is-indeterminate' : ''} style={phase === 'processing' ? undefined : {width: `${progress}%`}}/>
          </div>
        </div> : <div className="dropzone-meta-wrap">
          <span>PDF, Word (.docx, .doc), or Text documents</span>
          <span className="dropzone-tip">Note: Avoid uploading very heavy size documents for faster processing</span>
        </div>}
      </button>
      <input ref={input} type="file" accept=".pdf,.docx,.doc,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword,text/plain" hidden onChange={e => {select(e.target.files?.[0]);e.target.value=''}}/>
      <div className="welcome-points"><span>01 <b>Scan every page</b></span><span>02 <b>Build a concise briefing</b></span><span>03 <b>Explore terms in context</b></span></div>
    </div>
    <div className="welcome-footer">PRIVATE BY DESIGN <i/> YOUR DOCUMENT STAYS IN THIS SESSION</div>
  </main>
}
