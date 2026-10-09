const categories = [
  { key: 'scientist', label: 'Scientists' },
  { key: 'person', label: 'People' },
  { key: 'scientific-term', label: 'Science terms' },
  { key: 'location', label: 'Places' },
]

export default function HighlightLegend({ enabled, onToggle }) {
  return (
    <div className="top-highlight-legend" aria-label="Color key">
      <button
        type="button"
        role="switch"
        aria-checked={enabled}
        className={`top-highlight-toggle ${enabled ? 'is-on' : ''}`}
        onClick={onToggle}
        title="Toggle color key highlighting"
      >
        <span className="top-highlight-toggle-knob" />
        <span className="top-highlight-label">Color key: <b>{enabled ? 'On' : 'Off'}</b></span>
      </button>
      <div className={`top-legend-items ${enabled ? '' : 'is-disabled'}`}>
        {categories.map(item => (
          <span key={item.key} className={`top-legend-item ${item.key}`}>
            <span className={`highlight-swatch ${item.key}`} aria-hidden="true" />
            <span className="top-legend-text">{item.label}</span>
          </span>
        ))}
      </div>
    </div>
  )
}
