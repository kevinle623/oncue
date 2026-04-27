import { Divider } from "@/components/common/divider";
import { Footer } from "@/components/layout/footer";
import { Nav } from "@/components/layout/nav";
import { Faq } from "@/components/sections/faq";
import { GetStartedCta } from "@/components/sections/get-started-cta";
import { Hero } from "@/components/sections/hero";
import { HowItWorks } from "@/components/sections/how-it-works";
import { Integrations } from "@/components/sections/integrations";
import { Privacy } from "@/components/sections/privacy";
import { WhyHandsFree } from "@/components/sections/why-hands-free";

export default function Home() {
  return (
    <>
      <Nav />
      <main className="flex-1">
        <Hero />
        <Divider />
        <HowItWorks />
        <Divider />
        <Integrations />
        <WhyHandsFree />
        <Privacy />
        <Faq />
        <GetStartedCta />
      </main>
      <Footer />
    </>
  );
}
