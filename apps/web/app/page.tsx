import { Footer } from "@/components/layout/footer";
import { Nav } from "@/components/layout/nav";
import { FinalCta } from "@/components/sections/final-cta";
import { Hero } from "@/components/sections/hero";
import { HowItWorks } from "@/components/sections/how-it-works";
import { Integrations } from "@/components/sections/integrations";
import { UseCases } from "@/components/sections/use-cases";

export default function Home() {
  return (
    <>
      <Nav />
      <main className="flex-1">
        <Hero />
        <HowItWorks />
        <UseCases />
        <Integrations />
        <FinalCta />
      </main>
      <Footer />
    </>
  );
}
