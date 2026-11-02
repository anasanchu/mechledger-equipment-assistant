import { useEffect, useMemo, useRef, useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { AlertCircle, BookOpen, CheckCircle2, Download, FileText, LoaderCircle, MessageSquare, Plus, RotateCw, Send, Trash2, Upload, X } from 'lucide-react';
import './App.css';

const API_BASE = (import.meta.env.VITE_API_BASE || 'http://localhost:8002').replace(/\/$/, '');
const makeCase = () => ({
  id: `case-${globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`}`,
  title: 'New conversation',
  messages: [],
});

function loadCases() {
  try {
    const saved = JSON.parse(localStorage.getItem('mechledger_cases') || 'null');
    if (Array.isArray(saved) && saved.length) return saved.map(item => ({
      id: String(item.id),
      title: item.title || 'Conversation',
      messages: (item.messages || []).filter(message => typeof message.content === 'string' && ['user', 'assistant', 'ai'].includes(message.role)).map(message => ({
        role: message.role === 'ai' ? 'assistant' : message.role,
        content: message.content,
      })),
    }));
    const oldChats = JSON.parse(localStorage.getItem('pike_rag_chats') || 'null');
    if (Array.isArray(oldChats) && oldChats.length) return oldChats.map(item => ({
      id: String(item.id),
      title: item.title || 'Imported conversation',
      messages: (item.messages || []).filter(message => typeof message.content === 'string' && ['user', 'assistant', 'ai'].includes(message.role)).map(message => ({
        role: message.role === 'ai' ? 'assistant' : message.role,
        content: message.content,
      })),
    }));
  } catch { /* Start a clean conversation if saved history is damaged. */ }
  return [makeCase()];
}

function friendlyError(error, fallback) {
  const status = error.response?.status;
  if (!error.response) return 'Cannot reach the MECHLEDGER server. Check that the app is running, then try again.';
  if (status === 409) return 'A file with this name is already in this conversation. Remove it first or choose another file.';
  if (status === 413) return 'This file is too large. Choose a file under 50 MB.';
  if (status === 400 && typeof error.response.data?.detail === 'string') return error.response.data.detail;
  return fallback;
}

function statusLabel(document) {
  if (document.status === 'ready' || document.indexed) return 'Ready';
  if (document.status === 'processing') return 'Preparing…';
  if (document.status === 'failed') return 'Needs attention';
  return 'Needs retry';
}

export default function App() {
  const [cases, setCases] = useState(loadCases);
  const [caseId, setCaseId] = useState(() => {
    const savedId = localStorage.getItem('mechledger_active_case') || localStorage.getItem('pike_rag_current_chat');
    return cases.some(item => item.id === savedId) ? savedId : cases[0].id;
  });
  const [documents, setDocuments] = useState([]);
  const [question, setQuestion] = useState('');
  const [notice, setNotice] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [thinking, setThinking] = useState(false);
  const [workingDocument, setWorkingDocument] = useState('');
  const picker = useRef(null);
  const thread = useRef(null);
  const activeCase = cases.find(item => item.id === caseId) || cases[0];
  const readyDocuments = useMemo(() => documents.filter(item => item.status === 'ready' || item.indexed), [documents]);

  useEffect(() => {
    localStorage.setItem('mechledger_cases', JSON.stringify(cases));
  }, [cases]);

  useEffect(() => {
    localStorage.setItem('mechledger_active_case', caseId);
    let stopped = false;
    let timer;
    const refreshDocuments = async () => {
      try {
        const response = await axios.get(`${API_BASE}/documents/status`, { params: { chat_id: caseId }, timeout: 10000 });
        if (stopped) return;
        const nextDocuments = response.data.documents || [];
        setDocuments(nextDocuments);
        if (response.data.warning) setNotice({ text: response.data.warning, kind: 'warning' });
        const processing = nextDocuments.some(item => item.status === 'processing');
        timer = window.setTimeout(refreshDocuments, processing ? 2500 : 12000);
      } catch {
        if (stopped) return;
        setNotice({ text: 'Cannot reach the app server. Your saved conversations are still here.', kind: 'error' });
        timer = window.setTimeout(refreshDocuments, 8000);
      }
    };
    setDocuments([]);
    refreshDocuments();
    return () => { stopped = true; window.clearTimeout(timer); };
  }, [caseId]);

  useEffect(() => {
    thread.current?.scrollTo({ top: thread.current.scrollHeight, behavior: 'smooth' });
  }, [activeCase.messages, thinking]);

  const updateMessages = (id, updater) => {
    setCases(previous => previous.map(item => item.id === id ? { ...item, messages: updater(item.messages) } : item));
  };

  const addConversation = () => {
    const newConversation = makeCase();
    setCases(previous => [newConversation, ...previous]);
    setCaseId(newConversation.id);
    setQuestion('');
    setNotice(null);
  };

  const deleteConversation = id => {
    const conversation = cases.find(item => item.id === id);
    if (!conversation) return;
    if (!window.confirm(`Delete “${conversation.title}”? Its saved messages will be removed from this browser.`)) return;

    const remaining = cases.filter(item => item.id !== id);
    const nextCases = remaining.length ? remaining : [makeCase()];
    const nextId = id === caseId ? nextCases[0].id : caseId;
    setCases(nextCases);
    if (id === caseId) setCaseId(nextId);
    localStorage.removeItem(`mechledger_equipment_${id}`);
    setNotice({ text: 'Conversation deleted.', kind: 'success' });

    // A server cleanup problem must not prevent the conversation disappearing.
    axios.delete(`${API_BASE}/chat/${id}`, { timeout: 10000 }).catch(() => {
      setNotice({ text: 'Conversation removed from this browser. The server could not clear its saved files; try again when the server is available.', kind: 'warning' });
    });
  };

  const upload = async event => {
    const file = event.target.files?.[0];
    if (!file) return;
    const extension = file.name.toLowerCase().split('.').pop();
    if (!['pdf', 'docx', 'txt'].includes(extension)) {
      setNotice({ text: 'Choose a PDF, Word document, or text file.', kind: 'error' });
      event.target.value = '';
      return;
    }
    if (file.size > 50 * 1024 * 1024) {
      setNotice({ text: 'This file is too large. Choose a file under 50 MB.', kind: 'error' });
      event.target.value = '';
      return;
    }

    setUploading(true);
    setNotice({ text: `Saving ${file.name}…`, kind: 'loading' });
    const form = new FormData();
    form.append('chat_id', caseId);
    form.append('file', file);
    try {
      const response = await axios.post(`${API_BASE}/upload`, form, { timeout: 120000 });
      setDocuments(previous => [
        ...previous.filter(item => item.filename !== response.data.filename),
        { filename: response.data.filename || file.name, status: response.data.status || 'processing', indexed: false, message: response.data.message },
      ]);
      setNotice({ text: 'Manual saved. MECHLEDGER is preparing it for search; you can keep working.', kind: 'success' });
    } catch (error) {
      setNotice({ text: friendlyError(error, 'The manual could not be saved. Try again or choose another file.'), kind: 'error' });
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  const retryDocument = async filename => {
    setWorkingDocument(filename);
    setDocuments(previous => previous.map(item => item.filename === filename ? { ...item, status: 'processing', message: 'Preparing your manual for search.' } : item));
    try {
      await axios.post(`${API_BASE}/documents/${caseId}/${encodeURIComponent(filename)}/process`, {}, { timeout: 10000 });
      setNotice({ text: 'Retry started. Your manual is being prepared.', kind: 'loading' });
    } catch (error) {
      setNotice({ text: friendlyError(error, 'Could not retry this manual. Try again in a moment.'), kind: 'error' });
      setDocuments(previous => previous.map(item => item.filename === filename ? { ...item, status: 'failed' } : item));
    } finally {
      setWorkingDocument('');
    }
  };

  const removeDocument = async filename => {
    if (!window.confirm(`Remove “${filename}” from this conversation?`)) return;
    setDocuments(previous => previous.filter(item => item.filename !== filename));
    try {
      const response = await axios.delete(`${API_BASE}/documents/${caseId}/${encodeURIComponent(filename)}`, { timeout: 10000 });
      setNotice({ text: response.data.message || 'Manual removed.', kind: 'success' });
    } catch {
      setNotice({ text: 'The manual disappeared from this list, but the server could not confirm its removal. Refresh the page and try again.', kind: 'warning' });
    }
  };

  const send = async event => {
    event.preventDefault();
    const prompt = question.trim();
    if (!prompt || thinking) return;
    if (!readyDocuments.length) {
      setNotice({ text: 'Add a manual and wait until it says “Ready” before asking a question.', kind: 'warning' });
      return;
    }
    const id = caseId;
    updateMessages(id, messages => [...messages, { role: 'user', content: prompt }]);
    setCases(previous => previous.map(item => item.id === id && item.title === 'New conversation'
      ? { ...item, title: prompt.slice(0, 38) }
      : item));
    setQuestion('');
    setThinking(true);
    setNotice({ text: 'Searching your manuals…', kind: 'loading' });
    try {
      const response = await axios.post(`${API_BASE}/query`, { question: prompt, chat_id: id }, { timeout: 120000 });
      updateMessages(id, messages => [...messages, { role: 'assistant', content: response.data.answer }]);
      setNotice({ text: 'Answer ready. Select a source link to open the manual page.', kind: 'success' });
    } catch (error) {
      updateMessages(id, messages => [...messages, {
        role: 'assistant',
        content: friendlyError(error, 'MECHLEDGER could not answer right now. Check the app connection and try again.'),
      }]);
      setNotice({ text: friendlyError(error, 'MECHLEDGER could not answer right now. Check the app connection and try again.'), kind: 'error' });
    } finally {
      setThinking(false);
    }
  };

  const openSource = href => {
    if (!href) return;
    const url = new URL(href, window.location.href);
    window.open(url.href, '_blank', 'noopener,noreferrer');
  };

  const downloadReport = async () => {
    try {
      const response = await axios.post(`${API_BASE}/reports/${caseId}`, {
        case_title: activeCase.title,
        equipment: {},
        problem: activeCase.messages.find(message => message.role === 'user')?.content || '',
        messages: activeCase.messages.filter(message => message.role === 'user' || message.role === 'assistant'),
        documents: documents.map(item => item.filename),
        remarks: '',
      }, { responseType: 'blob', timeout: 30000 });
      const url = URL.createObjectURL(response.data);
      const link = document.createElement('a');
      link.href = url;
      link.download = `MECHLEDGER-${caseId.slice(-6)}-report.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
      setNotice({ text: 'Report downloaded.', kind: 'success' });
    } catch (error) {
      setNotice({ text: friendlyError(error, 'Could not create the report. Try again.'), kind: 'error' });
    }
  };

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-icon"><BookOpen size={17}/></span><span><b>MECHLEDGER</b><small>Equipment assistant</small></span></div>
      <button className="new-conversation" onClick={addConversation}><Plus size={17}/> New conversation</button>
      <div className="sidebar-label">CONVERSATIONS</div>
      <div className="conversation-list">
        {cases.map(item => <div key={item.id} className={`conversation-row ${item.id === caseId ? 'active' : ''}`}>
          <button className="conversation-select" onClick={() => { setCaseId(item.id); setQuestion(''); setNotice(null); }} title={item.title}>
            <MessageSquare size={15}/><span>{item.title}</span>
          </button>
          <button className="delete-conversation" onClick={() => deleteConversation(item.id)} aria-label={`Delete conversation ${item.title}`} title="Delete conversation"><Trash2 size={15}/></button>
        </div>)}
      </div>
      <div className="sidebar-footer">Your conversations are saved in this browser.</div>
    </aside>

    <main className="main-panel">
      <header className="topbar">
        <div><span className="eyebrow">MECHLEDGER</span><h1>{activeCase.title === 'New conversation' ? 'Equipment assistant' : activeCase.title}</h1></div>
        <div className="topbar-actions">
          {activeCase.messages.some(message => message.role === 'user') && <button className="secondary-button" onClick={downloadReport}><Download size={16}/> Report</button>}
          <button className="primary-button" onClick={() => picker.current?.click()} disabled={uploading}><Upload size={16}/>{uploading ? 'Saving…' : 'Add a manual'}</button>
          {activeCase.messages.length > 0 && <button className="delete-active" onClick={() => deleteConversation(caseId)}><Trash2 size={16}/><span>Delete conversation</span></button>}
        </div>
      </header>

      {notice && <div className={`notice notice-${notice.kind}`} role={notice.kind === 'error' ? 'alert' : 'status'}>
        {notice.kind === 'success' ? <CheckCircle2 size={17}/> : notice.kind === 'error' || notice.kind === 'warning' ? <AlertCircle size={17}/> : <LoaderCircle className={notice.kind === 'loading' ? 'spin' : ''} size={17}/>}
        <span>{notice.text}</span><button onClick={() => setNotice(null)} aria-label="Dismiss message"><X size={16}/></button>
      </div>}

      <div className="documents-bar" aria-label="Manuals in this conversation">
        <div className="documents-title"><FileText size={16}/><b>Manuals</b><span>{documents.length}</span></div>
        {documents.length ? <div className="document-chips">
          {documents.map(item => <div className={`document-chip chip-${item.status || 'needs_retry'}`} key={item.filename}>
            {item.status === 'processing' ? <LoaderCircle className="spin" size={15}/> : item.status === 'ready' || item.indexed ? <CheckCircle2 size={15}/> : <AlertCircle size={15}/>}
            <span className="chip-name" title={item.filename}>{item.filename}</span>
            <span className="chip-status">{statusLabel(item)}</span>
            {item.status === 'failed' || item.status === 'needs_retry' ? <button onClick={() => retryDocument(item.filename)} disabled={workingDocument === item.filename} aria-label={`Retry ${item.filename}`} title="Retry"><RotateCw size={14}/></button> : null}
            <button onClick={() => removeDocument(item.filename)} aria-label={`Remove ${item.filename}`} title="Remove manual"><X size={14}/></button>
            {item.status === 'failed' && item.message && <span className="document-help">{item.message}</span>}
          </div>)}
        </div> : <button className="inline-add" onClick={() => picker.current?.click()} disabled={uploading}><Plus size={15}/> Add a manual</button>}
      </div>

      <section className="chat-area">
        {!activeCase.messages.length ? <div className="welcome-card">
          <div className="welcome-icon"><BookOpen size={25}/></div>
          <h2>Ask about your equipment</h2>
          <p>1. Add a manual. &nbsp; 2. Describe the problem. &nbsp; 3. Check the linked source page.</p>
          <button className="primary-button welcome-button" onClick={() => picker.current?.click()} disabled={uploading}><Upload size={16}/> Choose a manual</button>
          <small>PDF, DOCX or TXT · Up to 50 MB</small>
        </div> : <div className="messages" ref={thread}>
          {activeCase.messages.map((message, index) => <article className={`message message-${message.role}`} key={`${index}-${message.content.slice(0, 20)}`}>
            {message.role === 'user' ? <div className="user-bubble">{message.content}</div> : <div className="assistant-message"><div className="assistant-label"><BookOpen size={15}/> MECHLEDGER</div><div className="markdown-answer"><ReactMarkdown components={{ a: ({ href, children, ...props }) => <a href={href} onClick={event => { event.preventDefault(); openSource(href); }} {...props}>{children}</a> }}>{message.content}</ReactMarkdown></div></div>}
          </article>)}
          {thinking && <div className="thinking"><LoaderCircle className="spin" size={16}/> Looking through your manuals…</div>}
        </div>}
      </section>

      <div className="composer-area">
        <form className="composer" onSubmit={send}>
          <textarea value={question} onChange={event => setQuestion(event.target.value)} placeholder={readyDocuments.length ? 'Describe the problem or ask a question…' : 'Add a manual and wait until it is ready to ask'} rows={2} disabled={!readyDocuments.length || thinking} onKeyDown={event => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); send(event); } }}/>
          <button className="send-button" type="submit" disabled={!question.trim() || !readyDocuments.length || thinking} aria-label="Send question"><Send size={17}/></button>
        </form>
        <div className="composer-help"><span>Answers use your manuals and include source links when available.</span><span>Enter to send · Shift + Enter for a new line</span></div>
      </div>
    </main>
    <input ref={picker} type="file" accept="application/pdf,.pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,.docx,text/plain,.txt" hidden disabled={uploading} onChange={upload}/>
  </div>;
}
