import styles from './ControlPanel.module.css'

const FIELDS = [
  { key: 'n_cities',      label: 'Şehir sayısı',      min: 4,  max: 50,   step: 1,    type: 'int' },
  { key: 'pop_size',      label: 'Popülasyon',         min: 5,  max: 100,  step: 5,    type: 'int' },
  { key: 'n_generations', label: 'Nesil sayısı',       min: 10, max: 1000, step: 10,   type: 'int' },
  { key: 'delta',         label: 'Rotasyon adımı (Δθ)',min: 0.01,max: 0.5, step: 0.01, type: 'float' },
  { key: 'seed',          label: 'Tohum (seed)',        min: 0,  max: 9999, step: 1,    type: 'int' },
]

export default function ControlPanel({ params, onChange, onSolve, loading }) {
  function handleChange(key, type, value) {
    onChange({ ...params, [key]: type === 'float' ? parseFloat(value) : parseInt(value, 10) })
  }

  return (
    <div className={styles.panel}>
      <h2 className={styles.title}>Parametreler</h2>

      {FIELDS.map(({ key, label, min, max, step, type }) => (
        <div key={key} className={styles.field}>
          <div className={styles.labelRow}>
            <label htmlFor={key}>{label}</label>
            <span className={styles.value}>{params[key]}</span>
          </div>
          <input
            id={key}
            type="range"
            min={min}
            max={max}
            step={step}
            value={params[key]}
            onChange={(e) => handleChange(key, type, e.target.value)}
            disabled={loading}
          />
        </div>
      ))}

      <button
        className={styles.solveBtn}
        onClick={onSolve}
        disabled={loading}
      >
        {loading ? 'Hesaplanıyor…' : '▶ Çöz'}
      </button>
    </div>
  )
}
