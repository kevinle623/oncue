import { Container } from "@/components/common/container";
import { CtaButton } from "@/components/common/cta-button";
import { RadialGlow } from "@/components/common/radial-glow";
import { Section } from "@/components/common/section";

export function FinalCta() {
  return (
    <Section>
      <RadialGlow className="opacity-60" />
      <Container className="text-center">
        <h2 className="font-heading text-5xl font-black tracking-[-0.05em] md:text-7xl lg:text-9xl">
          Drive. Talk. Done.
        </h2>
        <p className="text-muted-foreground mx-auto mt-8 max-w-xl text-lg leading-relaxed md:text-xl">
          Join the waitlist for the most sophisticated voice assistant ever
          built for the road. Early access slots opening monthly.
        </p>
        <div className="mt-10 flex justify-center">
          <CtaButton className="px-12 py-5 text-sm">Get early access</CtaButton>
        </div>
      </Container>
    </Section>
  );
}
