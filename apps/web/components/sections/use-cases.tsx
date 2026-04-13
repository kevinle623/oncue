import { Home, Music } from "lucide-react";
import { Container } from "@/components/common/container";
import { Section } from "@/components/common/section";
import { cn } from "@/lib/utils";

type UseCase = {
  icon: React.ComponentType<{ className?: string }>;
  quote: string;
  caption: string;
  imageGradient: string;
};

const cases: UseCase[] = [
  {
    icon: Music,
    quote: "Shuffle my late night drive playlist and set volume to 40%.",
    caption: "Works with Spotify & Apple Music",
    imageGradient:
      "radial-gradient(ellipse at 30% 30%, rgba(255,181,71,0.25), transparent 55%), radial-gradient(ellipse at 70% 80%, rgba(255,181,71,0.12), transparent 60%), linear-gradient(135deg, #1c1b1c, #0e0e0f)",
  },
  {
    icon: Home,
    quote: "Turn on the driveway lights and preheat the oven to 400.",
    caption: "Connected to HomeKit & Google Home",
    imageGradient:
      "radial-gradient(ellipse at 70% 40%, rgba(255,181,71,0.22), transparent 55%), radial-gradient(ellipse at 20% 80%, rgba(214,196,175,0.08), transparent 60%), linear-gradient(135deg, #131314, #1c1b1c)",
  },
];

export function UseCases() {
  return (
    <div id="showcase">
      {cases.map((useCase, i) => (
        <Section key={i}>
          <Container>
            <UseCaseRow {...useCase} reverse={i % 2 === 1} />
          </Container>
        </Section>
      ))}
    </div>
  );
}

function UseCaseRow({
  icon: Icon,
  quote,
  caption,
  imageGradient,
  reverse,
}: UseCase & { reverse?: boolean }) {
  return (
    <div
      className={cn(
        "flex flex-col items-center gap-12 md:flex-row md:gap-16",
        reverse && "md:flex-row-reverse",
      )}
    >
      <div className="flex-1 space-y-8">
        <div className="border-border bg-surface-high inline-flex rounded-lg border p-4">
          <Icon className="text-accent size-7" />
        </div>
        <blockquote className="font-heading text-3xl leading-tight font-extrabold tracking-tight md:text-5xl">
          &ldquo;{quote}&rdquo;
        </blockquote>
        <p className="text-muted-foreground text-sm tracking-[0.2em] uppercase">
          {caption}
        </p>
      </div>
      <div
        aria-hidden
        className="border-border aspect-video w-full flex-1 overflow-hidden rounded-xl border"
        style={{ background: imageGradient }}
      />
    </div>
  );
}
