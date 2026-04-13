import { Container } from "@/components/common/container";
import { CtaButton } from "@/components/common/cta-button";
import { Eyebrow } from "@/components/common/eyebrow";
import { RadialGlow } from "@/components/common/radial-glow";
import { Section } from "@/components/common/section";
import { Footer } from "@/components/layout/footer";
import { Nav } from "@/components/layout/nav";

export default function NotFound() {
  return (
    <>
      <Nav />
      <main className="flex-1">
        <Section>
          <RadialGlow />
          <Container className="text-center">
            <Eyebrow tone="accent">Error 404</Eyebrow>
            <h1 className="font-heading mt-6 text-7xl font-black tracking-[-0.05em] md:text-9xl">
              Off the map.
            </h1>
            <p className="text-muted-foreground mx-auto mt-8 max-w-lg text-lg leading-relaxed">
              This route doesn&apos;t exist yet. Head back to the main line.
            </p>
            <div className="mt-10 flex justify-center">
              <CtaButton href="/">Back to home</CtaButton>
            </div>
          </Container>
        </Section>
      </main>
      <Footer />
    </>
  );
}
