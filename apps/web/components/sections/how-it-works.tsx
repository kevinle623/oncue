import { Container } from "@/components/common/container";
import { Section } from "@/components/common/section";
import { SectionHeading } from "@/components/common/section-heading";
import { Card } from "@/components/ui/card";

const steps = [
  {
    n: "01",
    title: "Connect",
    body: "Save OnCue to your speed dial. No apps to open, no screens to unlock. A direct line to action.",
  },
  {
    n: "02",
    title: "Voice-Only",
    body: "Speak naturally. Our neural engine filters road noise and understands context, intent, and nuance.",
  },
  {
    n: "03",
    title: "Execute",
    body: "From messaging to navigation and smart home control. Everything happens instantly, on your command.",
  },
];

export function HowItWorks() {
  return (
    <Section id="how" className="bg-surface-low">
      <Container>
        <SectionHeading eyebrow="Protocol" title="Intelligence in motion." />
        <div className="bg-border mt-16 grid gap-px md:grid-cols-3">
          {steps.map((step) => (
            <Card
              key={step.n}
              className="bg-surface-low hover:bg-surface rounded-none border-0 px-10 py-10 ring-0 transition-colors"
            >
              <span
                aria-hidden
                className="font-heading text-foreground/5 text-6xl font-black"
              >
                {step.n}
              </span>
              <h3 className="font-heading text-xl font-bold tracking-tight uppercase">
                {step.title}
              </h3>
              <p className="text-muted-foreground leading-relaxed">
                {step.body}
              </p>
            </Card>
          ))}
        </div>
      </Container>
    </Section>
  );
}
