import Counter from "@/component/Counter";
import styles from './page.module.css'

export default function Home() {
  // Set a specific target date instead of relative time
  const targetDate = new Date('2025-07-06T09:25:00').getTime();
  // For testing purposes you can use this instead:
  // const targetDate = new Date().getTime() + (24 * 60 * 60 * 1000);

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>COMING SOON...</h1>
        <Counter targetDate={targetDate} />
      </div>
    </main>
  )
}
