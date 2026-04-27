import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { Reveal } from "@/components/common/reveal";
import { Section } from "@/components/common/section";
import { SectionBody } from "@/components/common/section-body";
import { SectionLabel } from "@/components/common/section-label";
import { SpotifyBadge } from "@/components/icons/brand/spotify";

type RoadmapItem = { name: string; tag: string; live?: boolean };

const ROADMAP: RoadmapItem[] = [
  { name: "Hosted app (no setup)", tag: "Soon", live: true },
  { name: "Trip Planning", tag: "2026" },
  { name: "Food & Coffee Orders", tag: "2026" },
  { name: "Smart Home", tag: "Later" },
];

export function Integrations() {
  return (
    <Section tone="surface-low">
      <Container>
        <Reveal>
          <SectionLabel>What it controls today</SectionLabel>
          <DisplayHeading className="mt-5">
            Start with <em>music.</em>
            <br />
            The rest is coming.
          </DisplayHeading>
          <SectionBody className="mt-5">
            Spotify is live in the open-source build. More integrations land as
            they&apos;re ready — each one has to work perfectly before it ships.
          </SectionBody>
        </Reveal>

        <div className="mt-14 flex flex-col gap-8 md:flex-row md:items-start md:gap-20">
          <Reveal className="md:flex-none">
            <LiveCard />
          </Reveal>
          <Reveal delay={100} className="md:flex-1">
            <p className="font-display text-muted-foreground mb-5 text-[13px] tracking-[0.08em] uppercase">
              On the roadmap
            </p>
            <ul className="flex flex-col gap-3">
              {ROADMAP.map((item) => (
                <li
                  key={item.name}
                  className="bg-surface border-border flex items-center gap-3.5 rounded-md border px-[18px] py-3.5"
                >
                  <span
                    className={
                      item.live
                        ? "size-2 shrink-0 rounded-full bg-[#1A1814] opacity-50"
                        : "bg-muted size-2 shrink-0 rounded-full"
                    }
                  />
                  <span className="text-foreground flex-1 text-sm">
                    {item.name}
                  </span>
                  <span className="text-muted-foreground border-border rounded-[2px] border px-2 py-[3px] text-[10px] font-medium tracking-[0.1em] uppercase">
                    {item.tag}
                  </span>
                </li>
              ))}
            </ul>
          </Reveal>
        </div>
      </Container>
    </Section>
  );
}

function LiveCard() {
  return (
    <div className="bg-surface border-border-strong w-full rounded-lg border p-7 md:w-[240px]">
      <p className="text-accent mb-5 text-[10px] font-medium tracking-[0.16em] uppercase">
        Live now
      </p>
      <div className="mb-[18px] flex items-center gap-2.5">
        <SpotifyBadge />
        <span className="text-foreground text-lg font-medium">Spotify</span>
      </div>
      <p className="text-muted-foreground text-[13px] leading-[1.6] [&_strong]:text-foreground [&_strong]:font-normal">
        <strong>&ldquo;Play something to focus.&rdquo;</strong>
        <br />
        <strong>&ldquo;Skip.&rdquo;</strong>
        <br />
        <strong>&ldquo;Turn it down a bit.&rdquo;</strong>
        <br />
        <strong>&ldquo;What&apos;s this song?&rdquo;</strong>
      </p>
    </div>
  );
}
