import styles from './ResultPanel.module.css'

export default function ResultPanel({ result, elapsedMs, error }) {
  if (error) {
    return (
      <div className={`${styles.panel} ${styles.error}`}>
        <strong>Hata:</strong> {error}
      </div>
    )
  }

  if (!result) return null

  const stats = [
    { label: 'En İyi Mesafe', value: `${result.best_distance.toFixed(2)} birim` },
    { label: 'Şehir Sayısı', value: result.n_cities },
    { label: 'Popülasyon', value: result.pop_size },
    { label: 'Nesil Sayısı', value: result.n_generations },
    { label: 'Hesaplama Süresi', value: `${(elapsedMs / 1000).toFixed(2)} s` },
  ]

  return (
    <div className={styles.panel}>
      {stats.map(({ label, value }) => (
        <div key={label} className={styles.stat}>
          <span className={styles.label}>{label}</span>
          <span className={styles.value}>{value}</span>
        </div>
      ))}
    </div>
  )
}
