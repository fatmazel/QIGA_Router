import { useState } from 'react'
import ControlPanel from './components/ControlPanel'
import MapView from './components/MapView'
import FitnessChart from './components/FitnessChart'
import ResultPanel from './components/ResultPanel'
import { solveTSP } from './api/client'
import styles from './App.module.css'

const DEFAULT_PARAMS = {
  n_cities: 10,
  pop_size: 20,
  n_generations: 100,
  delta: 0.05,
  seed: 42,
}

export default function App() {
  const [params, setParams] = useState(DEFAULT_PARAMS)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [elapsedMs, setElapsedMs] = useState(0)

  async function handleSolve() {
    setLoading(true)
    setError(null)
    const t0 = performance.now()
    try {
      const data = await solveTSP(params)
      setElapsedMs(performance.now() - t0)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <h1>QIGA-Router</h1>
        <p>Quantum-Inspired Genetic Algorithm · TSP Optimizer</p>
      </header>

      <main className={styles.main}>
        {/* Sol sütun: parametreler */}
        <aside className={styles.sidebar}>
          <ControlPanel
            params={params}
            onChange={setParams}
            onSolve={handleSolve}
            loading={loading}
          />
        </aside>

        {/* Sağ sütun: harita + grafik */}
        <section className={styles.content}>
          <ResultPanel result={result} elapsedMs={elapsedMs} error={error} />
          <MapView
            cities={result?.cities ?? null}
            route={result?.best_route ?? null}
          />
          <FitnessChart fitnessHistory={result?.fitness_history ?? null} />
        </section>
      </main>
    </div>
  )
}
