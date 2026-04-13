import { Home, Music } from "lucide-react";
import { Container } from "@/components/common/container";
import { Section } from "@/components/common/section";
import { FadedImage } from "@/components/illustrations/faded-image";
import { cn } from "@/lib/utils";

type UseCase = {
  icon: React.ComponentType<{ className?: string }>;
  quote: string;
  caption: string;
  image: { src: string; alt: string };
};

const cases: UseCase[] = [
  {
    icon: Music,
    quote: "Shuffle my late night drive playlist and set volume to 40%.",
    caption: "Works with Spotify & Apple Music",
    image: {
      src: "/images/use-case-music.png",
      alt: "Interior of a luxury modern car at night with illuminated dashboard and bokeh city lights in the background",
    },
  },
  {
    icon: Home,
    quote: "Turn on the driveway lights and preheat the oven to 400.",
    caption: "Connected to HomeKit & Google Home",
    image: {
      src: "/images/use-case-home.png",
      alt: "Minimalist modern house exterior at dusk with warm interior lighting glowing through large glass windows",
    },
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
  image,
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
      <FadedImage
        src={image.src}
        alt={image.alt}
        fill
        sizes="(min-width: 768px) 50vw, 100vw"
        className="group aspect-video w-full flex-1"
        imageClassName="grayscale transition-all duration-700 group-hover:grayscale-0"
      />
    </div>
  );
}
