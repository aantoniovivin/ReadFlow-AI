export function normalizeParagraphText(value) {
  if (!value) return ''
  let text = String(value)
    // Normalize unicode compatibility ligatures (fi, fl, ffi, etc.)
    .normalize('NFKC')
    // Remove null bytes, replacement characters, zero-width spaces
    .replace(/[\u0000\ufffd\u200B-\u200D\uFEFF]/g, '')
    // Fix HTML entities
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"')
    // Fix broken hyphenation at line breaks (e.g. "com-\nputer" -> "computer")
    .replace(/(?<=[A-Za-z])-\s*\n\s*(?=[a-z])/g, '')
    .replace(/(?<=[A-Za-z])-\s+(?=[a-z])/g, '')
    // Fix soft line breaks in the middle of a sentence (join broken lines without merging separate paragraphs)
    .replace(/([^\n.!?])\n([a-z0-9A-Z])/g, '$1 $2')
    // Fix broken apostrophes/possessives
    .replace(/([A-Za-z0-9])\s*['’]\s*(s|d|ll|re|ve|m|t)\b/gi, '$1’$2')
    // Fix spacing before punctuation
    .replace(/\s+([.,;:!?])/g, '$1')
    // Fix repeated punctuation
    .replace(/\.{2,}/g, '.')
    // Fix spacing inside brackets and parentheses
    .replace(/\(\s+/g, '(')
    .replace(/\s+\)/g, ')')
    .replace(/\[\s+/g, '[')
    .replace(/\s+\]/g, ']')
    // Fix broken decimal numbers (e.g. "1 . 1" -> "1.1", "1 . 1 . 2" -> "1.1.2")
    .replace(/\b(\d+)\s*\.\s*(\d+)\b/g, '$1.$2')
    // Fix double spaces
    .replace(/[ \t]+/g, ' ')
    .trim()

  return text
}

export function cleanDocumentText(value) {
  if (!value) return ''
  let text = normalizeParagraphText(value)
    // Remove leading bullet characters and symbols (•, ·, ●, ○, ■, ◆, ▪, ▫, ‣, ⁃, *, -, –)
    .replace(/^[\s•·●○■◆▪▫‣⁃\u2022\u00b7\u25cf\u25cb\u25aa\u25ab\u25b8\u2043\u2219\u25c6*–—\-]+\s*/, '')
    // Replace inline bullet symbols separating clauses with a period/space
    .replace(/\s*[•·●○■◆▪▫‣⁃\u2022\u00b7\u25cf\u25cb\u25aa\u25ab\u25b8\u2043\u2219\u25c6]\s*/g, '. ')
    // Fix spaced out single-letter gaps (e.g. "l i n n a e u s" -> "linnaeus")
    .replace(/\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b/g, '$1$2$3$4')
    // Strip dangling trailing conjunctions, prepositions, and incomplete endings
    .replace(/\s+(?:and|or|to|for|with|of|that|is|are|in|on|by|from|as|such as|called|which|because)\s*[.,:;]?$/i, '')
    // Fix trailing dangling punctuation (e.g. trailing comma, semicolon, dash)
    .replace(/[,;:\-–—\s]+$/, '')
    // Fix double spaces
    .replace(/[ \t]+/g, ' ')
    .trim()

  return text
}

export function capitalizeSentenceStarts(value) {
  const cleaned = cleanDocumentText(value)
  return cleaned.replace(/(^|[.!?]\s+|\n+)([\s"'“‘([{]*)([a-z])/g,
    (_match, boundary, prefix, letter) => `${boundary}${prefix}${letter.toUpperCase()}`)
}

const MINOR_WORDS = new Set(['a', 'an', 'and', 'as', 'at', 'by', 'for', 'from', 'in', 'into', 'of', 'on', 'or', 'the', 'to', 'with'])

export function toTitleCase(str) {
  if (!str) return ''
  const words = str.trim().split(/\s+/).filter(Boolean)
  return words.map((word, index) => {
    const lower = word.toLowerCase()
    if (index > 0 && MINOR_WORDS.has(lower)) {
      return lower
    }
    if (/^[A-Z0-9]{2,}$/.test(word)) return word
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  }).join(' ')
}

export function conciseDocumentHeading(title, keyIdeas) {
  let rawTitle = cleanDocumentText(title || '')

  // 1. Clean out page ranges, chapter prefixes, bullet points, numbers
  rawTitle = rawTitle
    .replace(/^(\d+(?:\.\d+)*|chapter\s+\d+|unit\s+\d+|part\s+\d+|module\s+\d+|section\s+\d+)(?:[:.\-–—]\s*|\s+)/i, '')
    .replace(/^summary\s*[·\-–—]\s*(?:pp?\.?\s*[\d–\-,\s]+)?/i, '')
    .replace(/^(?:pp?\.?\s*[\d–\-,\s]+)\s*[:.\-–—]?\s*/i, '')
    .replace(/[“"'”’]/g, '')
    .replace(/[:.\-–—]\s*$/, '')
    .trim()

  const isGeneric = !rawTitle || /^(?:summary|document\s+summary|overview|section\s*\d*|part\s*\d*|untitled|source\s+pages)$/i.test(rawTitle)

  if (!isGeneric) {
    let clean = rawTitle
      .replace(/\?+$/, '')
      .replace(/^(?:what\s+is|what\s+are)\s+/i, 'What Is ')
      .trim()
    
    const words = clean.split(/\s+/).filter(Boolean)
    if (words.length >= 1 && words.length <= 7) {
      return toTitleCase(clean)
    }
    if (words.length > 7) {
      const parts = clean.split(/[:\-–—|,]\s+/)
      if (parts[0] && parts[0].split(/\s+/).length >= 2 && parts[0].split(/\s+/).length <= 6) {
        return toTitleCase(parts[0])
      }
      let slice = words.slice(0, 5)
      while (slice.length > 1 && MINOR_WORDS.has(slice[slice.length - 1].toLowerCase())) {
        slice.pop()
      }
      return toTitleCase(slice.join(' '))
    }
  }

  const sources = [
    ...(Array.isArray(keyIdeas) ? keyIdeas : []),
    rawTitle
  ].map(cleanDocumentText).filter(Boolean)

  for (const src of sources) {
    let candidate = src
      .replace(/^(?:this\s+section|in\s+this\s+section|the\s+source|it\s+is\s+clear\s+that|we\s+can\s+see\s+that|organisms?\s+are|key\s+ideas?\s+include)\s+/i, '')
      .replace(/[“"'”’]/g, '')
      .split(/[:;.,!?]/)[0]
      .trim()

    const words = candidate.split(/\s+/).filter(Boolean)
    while (words.length && MINOR_WORDS.has(words[0].toLowerCase())) words.shift()
    
    if (words.length >= 2) {
      let slice = words.slice(0, Math.min(words.length, 5))
      while (slice.length > 1 && MINOR_WORDS.has(slice[slice.length - 1].toLowerCase())) {
        slice.pop()
      }
      if (slice.length >= 2) {
        return toTitleCase(slice.join(' '))
      }
    }
  }

  return 'Study Concepts'
}
