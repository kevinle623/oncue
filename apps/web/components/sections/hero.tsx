import { Container } from "@/components/common/container";
import { CtaButton } from "@/components/common/cta-button";
import { Eyebrow } from "@/components/common/eyebrow";
import { RadialGlow } from "@/components/common/radial-glow";
import { Section } from "@/components/common/section";
import { StatusDot } from "@/components/common/status-dot";
import { HeroVisual } from "@/components/illustrations/hero-visual";

export function Hero() {
  return (
    <Section className="pt-28 lg:pt-24">
      <RadialGlow />
      <Container>
        <div className="grid items-center gap-16 lg:grid-cols-2">
          <div className="space-y-8">
            <div className="flex items-center gap-3">
              <StatusDot pulse />
              <Eyebrow>Building in public</Eyebrow>
            </div>
            <h1 className="font-heading text-5xl leading-[0.9] font-black tracking-[-0.04em] md:text-7xl lg:text-[7rem]">
              Everything,
              <br />
              on cue.
            </h1>
            <p className="text-muted-foreground max-w-md text-lg leading-relaxed">
              The definitive voice interface for drivers. Connect your digital
              life to your dashboard without lifting a finger or taking your
              eyes off the asphalt.
            </p>
            <div className="flex flex-col gap-4 pt-2 sm:flex-row">
              <CtaButton disabled>Get early access</CtaButton>
              <CtaButton variant="outline" href="#how">
                View Demo
              </CtaButton>
            </div>
          </div>
          <HeroVisual />
        </div>
      </Container>
    </Section>
  );
}
