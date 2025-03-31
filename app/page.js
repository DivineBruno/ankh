import Counter from "@/component/Counter";
import Link from "next/link";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <Counter title="Counter #1"/>
        <Counter title="Counter #2"/>
        <Counter title="Counter #3"/>
      </main>
      <Link href="/dashboard" className="underline">
      Dashboard
      </Link>
    </div> 
  );
}
