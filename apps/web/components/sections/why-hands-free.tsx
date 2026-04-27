import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { Reveal } from "@/components/common/reveal";
import { Section } from "@/components/common/section";
import { SectionLabel } from "@/components/common/section-label";

type Stat = { num: string; label: string };

const STATS: Stat[] = [
  { num: "9×", label: "more crashes when dialing manually vs. hands-free" },
  { num: "5s", label: "average eyes-off-road time to skip a track" },
  { num: "88%", label: "of drivers admit to phone use while driving" },
  { num: "0", label: "screen interactions required with OnCue" },
];

export function WhyHandsFree() {
  return (
    <Section>
      <Container>
        <Reveal>
          <SectionLabel>Why hands-free matters</SectionLabel>
          <DisplayHeading className="mt-5">
            Eyes on the road.
            <br />
            <em>Always.</em>
          </DisplayHeading>
        </Reveal>

        <Reveal className="bg-border mt-14 grid grid-cols-2 gap-px overflow-hidden rounded border md:grid-cols-4">
          {STATS.map((stat) => (
            <div key={stat.num} className="bg-surface px-7 py-9">
              <div className="font-display text-accent mb-2.5 text-[clamp(36px,5vw,52px)] leading-none">
                {stat.num}
              </div>
              <p className="text-muted-foreground text-[13px] leading-[1.5] font-light">
                {stat.label}
              </p>
            </div>
          ))}
        </Reveal>

        <Reveal className="mt-14 grid grid-cols-1 gap-6 md:grid-cols-2 md:gap-12">
          <p className="text-muted-foreground text-base leading-[1.75] font-light [&_strong]:text-foreground [&_strong]:font-normal">
            We&apos;re not here to lecture you about your phone.{" "}
            <strong>We&apos;ve all glanced down at a red light.</strong>{" "}
            We&apos;ve all half-reached for the aux cord. OnCue exists because
            the phone doesn&apos;t disappear — but the friction can.
          </p>
          <p className="text-muted-foreground text-base leading-[1.75] font-light [&_strong]:text-foreground [&_strong]:font-normal">
            Hands-free isn&apos;t a feature.{" "}
            <strong>It&apos;s a constraint that forces better design.</strong>{" "}
            Every interaction in OnCue was built to be done in a single spoken
            sentence, at 70mph, with one eye on a merge.
          </p>
        </Reveal>
      </Container>
    </Section>
  );
}
