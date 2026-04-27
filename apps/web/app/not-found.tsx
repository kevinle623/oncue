import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { PrimaryButton } from "@/components/common/primary-button";
import { Section } from "@/components/common/section";
import { SectionLabel } from "@/components/common/section-label";
import { Footer } from "@/components/layout/footer";
import { Nav } from "@/components/layout/nav";

export default function NotFound() {
  return (
    <>
      <Nav />
      <main className="flex-1 pt-32">
        <Section>
          <Container className="text-center">
            <SectionLabel>Error 404</SectionLabel>
            <DisplayHeading as="h1" size="lg" className="mt-6">
              <em>Off the map.</em>
            </DisplayHeading>
            <p className="text-muted-foreground mx-auto mt-8 max-w-lg text-lg leading-relaxed font-light">
              This route doesn&apos;t exist yet. Head back to the main line.
            </p>
            <div className="mt-10 flex justify-center">
              <PrimaryButton href="/">Back to home</PrimaryButton>
            </div>
          </Container>
        </Section>
      </main>
      <Footer />
    </>
  );
}
