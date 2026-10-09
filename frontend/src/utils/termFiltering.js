const commonWords = new Set(`
  a an and are as at be been being but by can could did do does doing fig figs figure figures for from had has have
  he her hers him his how i if in into is it its may me might more most must my no nor not
  of on once only or other our out over own same she should so some such than that the their
  them then there these they this those through to too under until up very was we were what
  when where which while who whom why will with would you your
`.trim().split(/\s+/))

export function isMeaningfulTerm(value) {
  const words = String(value || '').toLocaleLowerCase().match(/[a-z]+/g) || []
  return words.length > 0 && !words.every(word => commonWords.has(word))
}
