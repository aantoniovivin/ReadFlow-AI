import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut } from 'lucide-react'
import { isMeaningfulTerm } from '../utils/termFiltering'

export default function DocumentViewer({ document, page, setPage, open, onClose, onSelectTerm }) {
  if (!open) return null
  const boxes = document.term_boxes.filter(box => box.page === page && isMeaningfulTerm(box.term))
  return <aside className="scan-drawer">
    <div className="scan-head"><div><span className="eyebrow">SOURCE DOCUMENT</span><h3>Original scan</h3></div><button className="icon-button" onClick={onClose}>×</button></div>
    <div className="scan-image-wrap">
      <img src={`/api/documents/${document.id}/pages/${page}.png`} alt={`Page ${page} of ${document.filename}`}/>
      <div className="scan-overlays">{boxes.map((b, i) => <div key={`${b.term}-${i}`} className={`scan-box ${(b.category || 'scientific_term').replace('_', '-')}`} role="button" tabIndex={0} aria-label={`Explain ${b.term}`} onClick={()=>onSelectTerm?.(b)} onKeyDown={event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();onSelectTerm?.(b)}}} style={{left:`${b.x*100}%`,top:`${b.y*100}%`,width:`${b.width*100}%`,height:`${b.height*100}%`}} title={`Click for meaning: ${b.term}`}/>)}</div>
    </div>
    <div className="scan-controls"><button className="icon-button" disabled={page<=1} onClick={()=>setPage(page-1)}><ChevronLeft/></button><span>Page <b>{page}</b> of {document.page_count}</span><button className="icon-button" disabled={page>=document.page_count} onClick={()=>setPage(page+1)}><ChevronRight/></button><i/><ZoomOut size={16}/><ZoomIn size={16}/></div>
    <div className="scan-thumbs">{Array.from({length:document.page_count}, (_,i)=><button key={i} className={page===i+1?'active':''} onClick={()=>setPage(i+1)}><img src={`/api/documents/${document.id}/pages/${i+1}.png`} alt=""/><span>{String(i+1).padStart(2,'0')}</span></button>)}</div>
    <p className="scan-note">Highlighted terms are linked to definitions in your briefing.</p>
  </aside>
}
