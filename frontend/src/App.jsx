import { useEffect, useRef, useState } from 'react'
import axios from 'axios'
const API_BASE_URL =
  import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});
import { AlertCircle, ArrowUpRight, BookOpen, Check, CheckCircle2, ChevronLeft, ChevronRight, ExternalLink, Eye, FileText, Globe, HelpCircle, Info, Layers3, LoaderCircle, Minus, Plus, RotateCcw, Search, Sparkles, Upload, X } from 'lucide-react'
import FileUpload from './components/FileUpload'
import DocumentViewer from './components/DocumentViewer'
import CleanSummaryReader from './components/CleanSummaryReader'
import HighlightLegend from './components/HighlightLegend'
import { conciseDocumentHeading } from './utils/heading'

function App() {
  const [doc,setDoc]=useState(null), [busy,setBusy]=useState(false), [uploadProgress,setUploadProgress]=useState(0), [uploadPhase,setUploadPhase]=useState('uploading'), [error,setError]=useState(''), [active,setActive]=useState(0), [sectionPreview,setSectionPreview]=useState(null), [previewPinned,setPreviewPinned]=useState(false), [dismissedPreview,setDismissedPreview]=useState(null), [railCollapsed,setRailCollapsed]=useState(false), [scanOpen,setScanOpen]=useState(false), [page,setPage]=useState(1), [hoverTerm,setHoverTerm]=useState(null), [termSummary,setTermSummary]=useState(''), [termSummaryTerm,setTermSummaryTerm]=useState(''), [termLoading,setTermLoading]=useState(false), [termError,setTermError]=useState(''), [termDetails,setTermDetails]=useState(null), [imageInfo,setImageInfo]=useState(null)
  const [colorMode,setColorMode]=useState(true)
  const [customSearch, setCustomSearch] = useState('')

  const SAMPLE_RANDOM_WORDS = [
    'Photosynthesis', 'Gravity', 'Atom', 'Neuron', 'CPU', 'Alluvial soil', 'Saturn', 'Carl Linnaeus', 'DNA', 'Organism', 'Primary memory', 'Compiler', 'Telescope'
  ]

  const handleCustomSearchSubmit = (e) => {
    e?.preventDefault()
    const q = customSearch.trim()
    if (!q) return
    setHoverTerm({ term: q, context: '' })
  }

  async function upload(file) {
    setError(''); setHoverTerm(null)
    const isSupported = /\.(pdf|docx|doc|txt)$/i.test(file?.name || '')
    if (!isSupported) { setError('Please choose a PDF, Word document (.docx, .doc), or Text file to continue.'); return }
    const form = new FormData()
    form.append('file', file)
    setBusy(true); setUploadProgress(0); setUploadPhase('uploading')
    try {
      const {data} = await api.post('/api/documents', form, {
        headers: {'Content-Type': 'multipart/form-data'},
        onUploadProgress: ({loaded, total}) => {
          if (!total) return
          const sent = loaded >= total
          setUploadProgress(Math.min(80, Math.round((loaded / total) * 80)))
          if (sent) {
            setUploadPhase('processing')
          }
        },
      })
      setUploadProgress(100); setDoc(data); setActive(0); setPage(1); setRailCollapsed(false)
    } catch (e) {
      setError(e.response?.data?.detail || 'We could not read this PDF. Please try another file.')
    } finally {
      setBusy(false)
    }
  }
  const brief=doc?.briefing
  useEffect(() => {
    if (!hoverTerm?.term) { setTermSummary(''); setTermSummaryTerm(''); setTermDetails(null); setImageInfo(null); return undefined }
    let cancelled = false
    setTermSummary(''); setTermSummaryTerm(''); setTermError(''); setTermDetails(null); setImageInfo(null); setTermLoading(true)
    async function loadTermInfo() {
      try {
        const payload = {
          term: hoverTerm.term,
          page: hoverTerm.page || null,
          section_index: hoverTerm.section_index ?? (active || 0),
          sentence: hoverTerm.context || '',
          resolved_entity: hoverTerm.resolved_entity || null,
          entity_type: hoverTerm.entity_type || null,
        }
        const endpoint = doc?.id ? `/api/documents/${doc.id}/terms/explain` : `/api/terms/explain`
        const {data} = await api.post(endpoint, payload)
        const explanation = simpleMeaning({
          term: hoverTerm.term,
          definition: extractMeaning(data),
          context: data.context || hoverTerm.context || '',
        })
        if (!cancelled) {
          setTermSummary('')
          setTermSummaryTerm(hoverTerm.term)
          setTermDetails({
            term: hoverTerm.term,
            entity: data.entity || null,
            entity_name: data.entity_name || data.entity?.name || hoverTerm.term,
            entity_type: data.entity_type || data.entity?.type || data.domain_topic || '',
            disambiguation: data.disambiguation || data.entity?.description || '',
            confidence: data.confidence ?? data.entity?.confidence ?? 1.0,
            is_ambiguous: Boolean(data.is_ambiguous),
            disambiguation_options: data.disambiguation_options || [],
            definition: data.definition || data.explanation?.definition || '',
            technical_explanation: data.explanation?.technical_explanation || data.technical_explanation || '',
            context_rationale: data.explanation?.context_rationale || data.disambiguation || '',
            reference_sentence: data.reference_sentence || data.web_reference_sentence || data.sentence || '',
            example: data.example || '',
            image: data.image || null,
            show_image: data.show_image ?? data.image?.show ?? false,
            real_image: data.image?.url || data.real_image || data.web_image || '',
            real_image_proxy: data.image?.proxy_url || data.real_image_proxy || data.web_image_proxy || '',
            image_title: data.image?.title || data.image_title || hoverTerm.term,
            image_provider: data.image?.source || data.image_provider || 'Pollinations AI',
            image_author: data.image?.author || '',
            image_license: data.image?.license || '',
            google_images_url: data.google_images_url || `https://www.google.com/search?tbm=isch&q=${encodeURIComponent(`${data.entity_name || data.entity?.name || hoverTerm.term} ${data.entity_type || ''}`.trim())}`,
            google_search_url: data.google_search_url || `https://www.google.com/search?q=${encodeURIComponent(`${data.entity_name || data.entity?.name || hoverTerm.term} ${data.entity_type || ''}`.trim())}`,
            source: data.source || null,
            source_url: data.source?.url || data.source_url || '',
            source_title: data.source?.title || data.source_title || '',
            source_provider: data.source?.provider || 'Wikipedia',
            domain_topic: data.domain_topic || data.entity_type || '',
            page: data.page || hoverTerm.page || null,
            root_word: data.root_word || hoverTerm.term,
            part_of_speech: data.part_of_speech || 'noun',
            svg_diagram: data.svg_diagram || '',
            doc_id: doc?.id || 'standalone',
          })
          if (data.web_reference) setImageInfo(data.web_reference)
        }
      } catch (e) {
        if (!cancelled && e.response?.status === 404 && doc?.id) {
          setHoverTerm(null)
          setDoc(null)
          setError('This document session expired when the backend restarted. Upload the PDF again to continue.')
        } else if (!cancelled) {
          setTermError(e.response?.data?.detail || e.message || 'Could not load the information. Please try again.')
        }
      } finally { if (!cancelled) setTermLoading(false) }
    }
    loadTermInfo()
    return () => { cancelled = true }
  }, [hoverTerm?.term, hoverTerm?.context, hoverTerm?.page, hoverTerm?.section_index, hoverTerm?.resolved_entity, hoverTerm?.entity_type, doc?.id, active])
  useEffect(() => {
    if (!hoverTerm) return undefined
    const closeOnOutside = event => {
      if (!event.target.closest('.definition-popover') && !event.target.closest('.scan-box') && !event.target.closest('.clickable-word') && !event.target.closest('.random-word-search-form')) setHoverTerm(null)
    }
    document.addEventListener('pointerdown', closeOnOutside)
    return () => document.removeEventListener('pointerdown', closeOnOutside)
  }, [hoverTerm])
  return <div className="app-shell">
    {doc ? <>
      <header className="topbar">
        <a className="brand" href="#" onClick={e=>{e.preventDefault();setDoc(null)}}><span className="brand-mark"><Layers3/></span><span>ReadFlow <em>AI</em></span></a>
        <span className="brand-divider"/>
        <div className="file-meta"><FileText/><b>{doc.filename}</b><span className="page-pill">{doc.page_count} pages</span></div>
        <form className="random-word-search-form" onSubmit={handleCustomSearchSubmit} style={{ display: 'flex', alignItems: 'center', gap: 6, margin: '0 12px' }}>
          <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
            <Search size={14} style={{ position: 'absolute', left: 10, color: '#94a3b8' }} />
            <input
              type="text"
              placeholder="Search or test any term…"
              value={customSearch}
              onChange={e => setCustomSearch(e.target.value)}
              style={{ padding: '6px 12px 6px 30px', fontSize: 13, borderRadius: 20, border: '1px solid #cbd5e1', outline: 'none', width: 210, background: '#f8fafc' }}
            />
          </div>
          <button type="submit" className="outline-button" style={{ padding: '5px 12px', fontSize: 12, borderRadius: 16 }}>Test Term</button>
        </form>
        <div className="top-actions">
          <HighlightLegend enabled={colorMode} onToggle={()=>setColorMode(v=>!v)}/>
          <span className="ready"><i/>{doc.ai_enabled?'AI briefing ready':'Briefing ready'}</span>
          <button className="outline-button" onClick={()=>setScanOpen(v=>!v)}><Eye size={17}/>{scanOpen?'Hide original':'Original document'}</button>
          <label className="primary-button"><Upload size={17}/> Upload document<input type="file" accept=".pdf,.docx,.doc,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword,text/plain" hidden onChange={e=>{upload(e.target.files?.[0]);e.target.value=''}}/></label>
        </div>
      </header>
      <div className="reader-layout"><aside className={`section-rail ${railCollapsed?'is-collapsed':''}`}><div className="rail-heading"><div className="rail-title">STUDY MODULES</div><button className="rail-toggle" type="button" aria-label={railCollapsed?'Expand section list':'Collapse section list'} title={railCollapsed?'Expand section list':'Collapse section list'} onClick={()=>setRailCollapsed(value=>!value)}>{railCollapsed?<ChevronRight size={16}/>:<ChevronLeft size={16}/>}</button></div><div className="section-list">{(brief?.sections || []).map((s,i)=><div className="section-card-wrap" key={i} onMouseEnter={()=>{if(!previewPinned&&dismissedPreview!==i)setSectionPreview(i)}} onMouseLeave={()=>{if(!previewPinned){setSectionPreview(null);setDismissedPreview(null)}}}><button onClick={()=>{setActive(i);setPreviewPinned(false);setSectionPreview(null);setDismissedPreview(null)}} onFocus={()=>{if(!previewPinned&&dismissedPreview!==i)setSectionPreview(i)}} onBlur={()=>{if(!previewPinned)setSectionPreview(null)}} className={`section-card ${active===i?'selected':''}`} aria-label={conciseDocumentHeading(s.title, s.key_takeaways?.length ? s.key_takeaways : s.takeaways)} title={railCollapsed?conciseDocumentHeading(s.title, s.key_takeaways?.length ? s.key_takeaways : s.takeaways):undefined} aria-describedby={sectionPreview===i?`section-preview-${i}`:undefined}><span className="section-number">{String(i+1).padStart(2,'0')}</span><span className="section-meta"><b>{conciseDocumentHeading(s.title, s.key_takeaways?.length ? s.key_takeaways : s.takeaways)}</b></span></button><button type="button" className="section-preview-trigger" aria-label={`Preview ${s.title}`} aria-expanded={sectionPreview===i&&previewPinned} onClick={()=>{if(previewPinned&&sectionPreview===i){setPreviewPinned(false);setSectionPreview(null);setDismissedPreview(i)}else{setSectionPreview(i);setDismissedPreview(null);setPreviewPinned(true)}}}><Info size={14}/></button>{sectionPreview===i&&<div className="section-card-preview" id={`section-preview-${i}`} role="status"><button className="section-preview-close" aria-label="Close section preview" onClick={()=>{setPreviewPinned(false);setSectionPreview(null);setDismissedPreview(i)}}><X size={14}/></button><span className="preview-eyebrow">MODULE {String(i+1).padStart(2,'0')}</span><strong>{conciseDocumentHeading(s.title, s.key_takeaways?.length ? s.key_takeaways : s.takeaways)}</strong><p>{s.subtitle||'Key ideas from this part of your document.'}</p><small>{s.key_takeaways?.[0]||s.takeaways?.[0]||s.foundational_overview||'Open this module to explore its summary.'}</small></div>}</div>)}</div><div className="rail-bottom"><span className="rail-check"><Check size={14}/></span><span><b>Briefing complete</b><small>{(doc.extracted_characters || 0).toLocaleString()} characters reviewed</small></span></div></aside>
        <main className={`reader-main ${scanOpen?'with-scan':''} ${railCollapsed?'rail-collapsed':''}`}><article className="paper"><CleanSummaryReader section={brief?.sections?.[active]||{title:'Document summary'}} sectionIndex={active} terms={brief?.terms||[]} colorMode={colorMode} onWordClick={({word,context,rect})=>setHoverTerm({term:word,context,section_index:active,doc_id:doc.id,anchor:{left:rect.left,top:rect.bottom}})}/><div className="paper-footer"><span>READFLOW AI <i/> SOURCE: {(doc.filename || 'DOCUMENT').toUpperCase()}</span><div><button onClick={()=>setActive(Math.max(0,active-1))} disabled={active===0}>Previous</button><span>{String(active+1).padStart(2,'0')} / {String((brief?.sections || []).length || 1).padStart(2,'0')}</span><button onClick={()=>setActive(Math.min((brief?.sections || []).length-1,active+1))} disabled={active>=(brief?.sections || []).length-1}>Next <ChevronRight size={15}/></button></div></div></article></main>
        <DocumentViewer document={doc} page={page} setPage={setPage} open={scanOpen} onClose={()=>setScanOpen(false)} onSelectTerm={termData=>setHoverTerm({...termData,doc_id:doc.id})}/>
      </div>
    </>:<><header className="welcome-top"><a className="brand" href="#"><span className="brand-mark"><Layers3/></span><span>ReadFlow <em>AI</em></span></a><span className="welcome-tag"><span/> DOCUMENT INTELLIGENCE</span></header>
      <FileUpload onUpload={upload} busy={busy} progress={uploadProgress} phase={uploadPhase}/>
      <div className="welcome-word-tester-wrap" style={{ maxWidth: 680, margin: '20px auto 40px auto', padding: '18px 24px', background: '#ffffff', borderRadius: 16, boxShadow: '0 4px 20px rgba(0,0,0,0.06)', border: '1px solid #e2e8f0', textAlign: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, marginBottom: 12 }}>
          <Sparkles size={16} color="#6366f1" />
          <b style={{ fontSize: 15, color: '#1e293b' }}>Instant Word &amp; Concept Visual Explorer</b>
        </div>
        <p style={{ fontSize: 13, color: '#64748b', margin: '0 0 14px 0' }}>Test any random term to generate its authoritative Wikipedia definition and accurate educational drawing:</p>
        <form className="random-word-search-form" onSubmit={handleCustomSearchSubmit} style={{ display: 'flex', gap: 8, justifyContent: 'center', maxWidth: 480, margin: '0 auto 14px auto' }}>
          <div style={{ position: 'relative', flex: 1, display: 'flex', alignItems: 'center' }}>
            <Search size={15} style={{ position: 'absolute', left: 12, color: '#94a3b8' }} />
            <input
              type="text"
              placeholder="e.g. Photosynthesis, Gravity, Atom, Neuron, CPU..."
              value={customSearch}
              onChange={e => setCustomSearch(e.target.value)}
              style={{ width: '100%', padding: '9px 14px 9px 34px', fontSize: 13.5, borderRadius: 10, border: '1px solid #cbd5e1', outline: 'none' }}
            />
          </div>
          <button type="submit" className="primary-button" style={{ padding: '8px 18px', fontSize: 13, borderRadius: 10 }}>Explore</button>
        </form>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, justifyContent: 'center', alignItems: 'center' }}>
          <span style={{ fontSize: 11, fontWeight: 600, color: '#94a3b8', textTransform: 'uppercase', marginRight: 4 }}>Quick Samples:</span>
          {SAMPLE_RANDOM_WORDS.map((w, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => setHoverTerm({ term: w, context: '' })}
              style={{ fontSize: 12, padding: '4px 10px', borderRadius: 14, border: '1px solid #e2e8f0', background: '#f8fafc', color: '#4338ca', cursor: 'pointer', fontWeight: 500 }}
            >
              {w}
            </button>
          ))}
        </div>
      </div>
      {error&&<div className="toast-error"><AlertCircle size={17}/>{error}<button onClick={()=>setError('')}><X size={15}/></button></div>}
    </>}
    {hoverTerm && (
      <DefinitionPopup
        key={`${hoverTerm.term}-${hoverTerm.context}-${hoverTerm.resolved_entity || ''}`}
        term={{ ...hoverTerm, ...(termDetails || {}) }}
        loading={termLoading}
        error={termError}
        imageInfo={imageInfo}
        onClose={() => setHoverTerm(null)}
        onSelectDisambiguation={(option) => {
          setHoverTerm(prev => ({
            ...prev,
            resolved_entity: option.entity_name || option.term || option.name,
            entity_type: option.entity_type,
          }))
        }}
      />
    )}
  </div>
}

function simpleMeaning(term) {
  const isFallback = /^(?:A key term detected|The document does not (?:clearly )?(?:define|provide enough context))/i.test(term.definition || '')
  const generated = term.definition && !isFallback
    ? term.definition
    : inferMeaningFromContext(term)
  if (!generated) return `The meaning of “${term.term}” could not be determined from the available context. Try selecting it in the original document.`
  const sentences = generated.trim().split(/(?<=[.!?])\s+/).filter(Boolean)
  const concise = sentences.slice(0, 2).join(' ')
  return concise.length > 300 ? `${concise.slice(0, 297).trimEnd()}…` : concise
}

function extractMeaning(payload, depth = 0) {
  if (depth > 4 || payload == null) return ''
  if (typeof payload === 'string') {
    const text = payload.trim()
    if (!text) return ''
    if (text.startsWith('{')) {
      try { return extractMeaning(JSON.parse(text), depth + 1) } catch { /* Keep plain response text. */ }
    }
    return text
  }
  if (Array.isArray(payload)) {
    for (const item of payload) {
      const found = extractMeaning(item, depth + 1)
      if (found) return found
    }
    return ''
  }
  for (const key of ['definition', 'meaning', 'explanation', 'answer', 'content', 'response']) {
    const found = extractMeaning(payload[key], depth + 1)
    if (found) return found
  }
  for (const key of ['data', 'result', 'message']) {
    const found = extractMeaning(payload[key], depth + 1)
    if (found) return found
  }
  if (payload.term && typeof payload.term === 'object') {
    return extractMeaning(payload.term, depth + 1)
  }
  return ''
}

function inferMeaningFromContext(term) {
  const escaped = term.term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const definition = term.context?.match(new RegExp(`${escaped}\\s+(?:is|are|means|refers to|describes)\\s+([^.;!?]+)`, 'i'))?.[1]
  return definition ? `${term.term} ${definition.trim()}.` : ''
}

function sentenceContext(text, start, end) {
  const boundaries = [...text.matchAll(/[.!?]\s+(?=[A-Z(])|\n+/g)]
  let contextStart = 0
  let contextEnd = text.length
  for (const boundary of boundaries) {
    const boundaryEnd = boundary.index + boundary[0].length
    if (boundaryEnd <= start) contextStart = boundaryEnd
    else if (boundary.index >= end) { contextEnd = boundary.index; break }
  }
  return text.slice(contextStart, contextEnd).trim()
}

function highlightTermInSentence(sentence, term) {
  if (!sentence || !term) return sentence || ''
  const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const regex = new RegExp(`(\\b${escaped}\\b)`, 'gi')
  const parts = sentence.split(regex)
  if (parts.length > 1) {
    return parts.map((part, i) =>
      part.toLowerCase() === term.toLowerCase()
        ? <mark key={i} className="sentence-term-highlight">{part}</mark>
        : part
    )
  }
  const fallbackRegex = new RegExp(`(${escaped})`, 'gi')
  const fallbackParts = sentence.split(fallbackRegex)
  if (fallbackParts.length > 1) {
    return fallbackParts.map((part, i) =>
      part.toLowerCase() === term.toLowerCase()
        ? <mark key={i} className="sentence-term-highlight">{part}</mark>
        : part
    )
  }
  return sentence
}

function DefinitionPopup({ term, loading, error, onClose, onSelectDisambiguation }) {
  const [position, setPosition] = useState(null)
  const [imageFailed, setImageFailed] = useState(false)
  const [useProxy, setUseProxy] = useState(false)
  const drag = useRef(null)

  useEffect(() => {
    setImageFailed(false)
    setUseProxy(false)
  }, [term.term, term.entity_name, term.real_image, term.image?.url])

  const definitionText = typeof term.definition === 'object' && term.definition !== null
    ? (term.definition.text || '')
    : (typeof term.definition === 'string' ? term.definition : (term.explanation?.definition || ''))

  const rawImageUrl = term.real_image || term.image?.url || ''
  const proxyImageUrl = term.real_image_proxy || term.image?.proxy_url || (rawImageUrl && term.doc_id ? `/api/documents/${term.doc_id}/image-proxy?url=${encodeURIComponent(rawImageUrl)}&term=${encodeURIComponent(term.entity_name || term.term)}` : '')
  const currentImageUrl = useProxy && proxyImageUrl ? proxyImageUrl : (rawImageUrl || proxyImageUrl)

  const beginDrag = (event) => {
    if (event.target.closest('button') || event.target.closest('a')) return
    event.preventDefault()
    const rect = event.currentTarget.closest('.definition-popover').getBoundingClientRect()
    drag.current = { x: event.clientX, y: event.clientY, left: rect.left, top: rect.top }
    event.currentTarget.setPointerCapture(event.pointerId)
  }
  const moveDrag = (event) => {
    if (!drag.current) return
    const rect = event.currentTarget.closest('.definition-popover').getBoundingClientRect()
    const left = Math.max(8, Math.min(window.innerWidth - rect.width - 8, drag.current.left + event.clientX - drag.current.x))
    const top = Math.max(8, Math.min(window.innerHeight - rect.height - 8, drag.current.top + event.clientY - drag.current.y))
    setPosition({ left, top })
  }
  const endDrag = () => {
    drag.current = null
    window.getSelection?.()?.removeAllRanges()
  }

  const showDisambiguation = Boolean((term.is_ambiguous || (term.disambiguation_options && term.disambiguation_options.length > 0)) && !term.resolved_entity)

  return (
    <aside
      className="definition-popover"
      style={position ? { left: position.left, top: position.top, right: 'auto', bottom: 'auto' } : undefined}
      role="dialog"
      aria-label={`Details for ${term.term}`}
    >
      <div
        className="definition-popover-heading"
        onPointerDown={beginDrag}
        onPointerMove={moveDrag}
        onPointerUp={endDrag}
        onPointerCancel={endDrag}
        onDoubleClick={() => setPosition(null)}
      >
        <BookOpen size={16} />
        <b>Word reference · drag to move</b>
        <button aria-label="Close" onClick={onClose}><X size={15} /></button>
      </div>

      <div style={{ marginTop: 4, marginBottom: 4 }}>
        <strong style={{ fontSize: 18, color: '#0f172a' }}>{term.term}</strong>
      </div>

      {/* Entity Badges: Resolved Entity, Type, Confidence */}
      <div className="entity-badge-container">
        {term.entity_name && term.entity_name.toLowerCase() !== term.term.toLowerCase() && (
          <span className="entity-badge">
            <Sparkles size={10} />
            {term.entity_name}
          </span>
        )}
        {term.entity_type && (
          <span className="entity-type-badge">
            {term.entity_type}
          </span>
        )}
        {term.confidence != null && term.confidence > 0 && (
          <span className="entity-confidence-badge" title="Disambiguation confidence">
            <CheckCircle2 size={10} />
            {Math.round(term.confidence * 100)}% match
          </span>
        )}
      </div>

      {(term.domain_topic || term.root_word || term.part_of_speech || term.page) && (
        <div className="term-context-meta">
          Root: {term.root_word || term.term} · Part of speech: {term.part_of_speech || 'noun'}
          {term.page ? ` · Page ${term.page}` : ''}
        </div>
      )}

      {/* In-Popup Authentic Photo Container */}
      {term.show_image !== false && currentImageUrl && !imageFailed && (
        <div
          className="term-popup-photo-card"
          style={{
            margin: '10px 0 8px 0',
            borderRadius: 8,
            overflow: 'hidden',
            border: '1px solid #e2e8f0',
            background: '#f8fafc',
            boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
            position: 'relative',
          }}
        >
          <div style={{ position: 'relative', width: '100%', height: 160, background: '#f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <img
              src={currentImageUrl}
              alt={term.entity_name || term.term}
              style={{
                width: '100%',
                height: 160,
                objectFit: 'cover',
                display: 'block',
              }}
              loading="eager"
              onError={() => {
                if (!useProxy && proxyImageUrl) {
                  setUseProxy(true)
                } else {
                  setImageFailed(true)
                }
              }}
            />
            {term.image_provider && (
              <span
                style={{
                  position: 'absolute',
                  bottom: 6,
                  right: 6,
                  background: 'rgba(15, 23, 42, 0.75)',
                  color: '#ffffff',
                  padding: '2px 8px',
                  borderRadius: 12,
                  fontSize: 10,
                  fontWeight: 500,
                  backdropFilter: 'blur(4px)',
                }}
              >
                {term.image_provider}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Interactive Disambiguation Options */}
      {showDisambiguation && (
        <div className="disambiguation-box" style={{ marginTop: 8, marginBottom: 8 }}>
          <div className="disambiguation-header">
            <HelpCircle size={12} />
            <b>Multiple meanings detected · Select context:</b>
          </div>
          <div className="disambiguation-options">
            {term.disambiguation_options.map((opt, idx) => (
              <button
                key={idx}
                type="button"
                className="disambiguation-option-btn"
                onClick={() => onSelectDisambiguation?.(opt)}
              >
                <span className="disambig-title">{opt.entity_name || opt.term}</span>
                <span className="disambig-desc">{opt.description || opt.entity_type}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Clean Definition Only */}
      {definitionText ? (
        <div className="term-detail-block" style={{ marginTop: 10, background: '#ffffff', padding: '14px 16px', borderRadius: 8, border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.04)' }}>
          <p style={{ margin: 0, fontSize: 13.5, lineHeight: 1.55, color: '#1e293b' }}>
            {definitionText}
          </p>
        </div>
      ) : loading ? (
        <div className="term-detail-block" style={{ marginTop: 10, padding: '14px 16px' }}>
          <p style={{ margin: 0, color: '#64748b', fontStyle: 'italic', display: 'flex', alignItems: 'center', gap: 6, fontSize: 13 }}>
            <LoaderCircle size={13} className="spin" /> Loading definition…
          </p>
        </div>
      ) : null}

      {error && <div className="term-image-placeholder" style={{ marginTop: 8 }}>{error}</div>}
    </aside>
  )
}

export default App
