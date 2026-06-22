import { useEffect, useRef, useState } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import { Line } from 'react-chartjs-2'
import styles from './FitnessChart.module.css'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const ANIMATION_INTERVAL_MS = 12  // her karede kaç ms beklenecek
const BATCH_SIZE = 5              // her karede kaç nesil eklenir

export default function FitnessChart({ fitnessHistory }) {
  const [displayed, setDisplayed] = useState([])
  const intervalRef = useRef(null)

  // Yeni sonuç geldiğinde animasyonu sıfırla ve yeniden başlat
  useEffect(() => {
    if (!fitnessHistory || fitnessHistory.length === 0) {
      setDisplayed([])
      return
    }

    clearInterval(intervalRef.current)
    setDisplayed([])

    let idx = 0
    intervalRef.current = setInterval(() => {
      idx += BATCH_SIZE
      if (idx >= fitnessHistory.length) {
        setDisplayed(fitnessHistory)
        clearInterval(intervalRef.current)
      } else {
        setDisplayed(fitnessHistory.slice(0, idx))
      }
    }, ANIMATION_INTERVAL_MS)

    return () => clearInterval(intervalRef.current)
  }, [fitnessHistory])

  const labels = displayed.map((_, i) => i + 1)

  const data = {
    labels,
    datasets: [
      {
        label: 'En İyi Mesafe',
        data: displayed,
        borderColor: '#4a6fa5',
        backgroundColor: 'rgba(74,111,165,0.12)',
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.3,
        fill: true,
      },
    ],
  }

  const options = {
    animation: false, // animasyonu manuel yapıyoruz
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (ctx) => ` ${ctx.parsed.y.toFixed(2)} birim`,
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: 'Nesil', color: '#718096' },
        ticks: { maxTicksLimit: 10, color: '#718096' },
        grid: { color: '#edf2f7' },
      },
      y: {
        title: { display: true, text: 'Mesafe', color: '#718096' },
        ticks: { color: '#718096' },
        grid: { color: '#edf2f7' },
      },
    },
  }

  return (
    <div className={styles.wrapper}>
      <h2 className={styles.title}>Yakınsama Grafiği</h2>

      {displayed.length === 0 ? (
        <div className={styles.placeholder}>
          Grafik çözüm sonrası burada canlanacak.
        </div>
      ) : (
        <Line data={data} options={options} />
      )}
    </div>
  )
}
