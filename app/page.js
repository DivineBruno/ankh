import Counter from "@/component/Counter";
import Link from "next/link";

export default function Home() {
  const isLoggedIn = true; 
  const name = "Bruno"; 

  console.log(process.env.MONGO_URI);

  return (
       <main>
          {/* HEADER */}
          <section className="bg-base-200"></section>

          {/* HERO */}
          <section className="text-center lg:text-left py-32 px-8 max-w-5xl mx-auto"></section>

          {/* PRICING */}
          <section className="bg-base-200"  id="pricing"> </section>

          {/* FAQ */}
          <section className="bg-base-200" id="faq"> </section>
      </main>
  );
}
