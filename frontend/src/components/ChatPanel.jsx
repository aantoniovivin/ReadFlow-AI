import { useState } from 'react'
import { Bot, Send, X } from 'lucide-react'
import axios from 'axios';

const API_BASE_URL =
  import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export default function ChatPanel({ document, onClose }) {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('Ask a question about this document and get an answer grounded in its text.')
  const [busy, setBusy] = useState(false)
  async function submit(e) { e.preventDefault(); if (!question.trim() || busy) return; setBusy(true); setAnswer('Searching your document…'); try { const {data}=await api.post(`/api/documents/${document.id}/chat`,{question}); setAnswer(data.answer) } catch { setAnswer('I could not reach the document service. Please try again.') } finally {setBusy(false);setQuestion('')} }
  return <div className="chat-panel"><div className="chat-title"><span className="chat-icon"><Bot size={16}/></span><div><b>Ask your document</b><small>Answers grounded in {document.filename}</small></div><button className="icon-button" onClick={onClose}><X size={17}/></button></div><p className="chat-answer">{answer}</p><form onSubmit={submit}><input value={question} onChange={e=>setQuestion(e.target.value)} placeholder="Ask anything about this PDF…"/><button disabled={busy||!question.trim()} aria-label="Send question"><Send size={16}/></button></form></div>
}
