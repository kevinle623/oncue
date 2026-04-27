import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { Reveal } from "@/components/common/reveal";
import { Section } from "@/components/common/section";

const POINTS = [
  "Calls are never recorded or used to train models. Audio is processed in real-time and discarded.",
  "You control which services OnCue can access. Revoke any integration from your account page, instantly.",
  "OnCue only acts on explicit commands. No passive listening, no background activity between calls.",
];

export function Privacy() {
  return (
    <Section tone="accent-soft" padding="compact">
      <Container>
        <div className="grid grid-cols-1 items-center gap-8 md:grid-cols-2 md:gap-16">
          <Reveal>
            <DisplayHeading size="sm">
              Your voice.
              <br />
              <em>Not our data.</em>
            </DisplayHeading>
            <p className="text-muted-foreground mt-4 text-[15px] leading-[1.7] font-light">
              Trust is a precondition for hands-free. We built the privacy model
              first, then the product.
            </p>
          </Reveal>
          <Reveal delay={100} className="flex flex-col gap-4">
            {POINTS.map((text) => (
              <PrivacyPoint key={text}>{text}</PrivacyPoint>
            ))}
          </Reveal>
        </div>
      </Container>
    </Section>
  );
}

function PrivacyPoint({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-start gap-4 rounded-md border border-[rgba(26,24,20,0.1)] bg-white/50 px-5 py-[18px]">
      <span className="border-accent mt-px flex size-5 shrink-0 items-center justify-center rounded-[3px] border">
        <svg viewBox="0 0 10 10" className="size-2.5" aria-hidden>
          <polyline
            points="2,5 4,7 8,3"
            stroke="#1A1814"
            fill="none"
            strokeWidth="2"
          />
        </svg>
      </span>
      <p className="text-foreground text-sm leading-[1.55] font-light">
        {children}
      </p>
    </div>
  );
}
