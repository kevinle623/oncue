import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { Reveal } from "@/components/common/reveal";
import { Section } from "@/components/common/section";
import { SectionLabel } from "@/components/common/section-label";

type Step = {
  num: string;
  title: string;
  body: string;
  icon: React.ReactNode;
};

const STEPS: Step[] = [
  {
    num: "01",
    title: "Dial with your voice",
    body: "\"Hey Siri, call OnCue.\" Any phone, any carrier, no internet — just a call. The voice agent you already have hands the rest to us.",
    icon: <PhoneIcon />,
  },
  {
    num: "02",
    title: "Speak naturally",
    body: '"Play something chill." "Skip this track." "Turn it up." OnCue understands you the way you actually talk.',
    icon: <WaveformIcon />,
  },
  {
    num: "03",
    title: "The assistant does it",
    body: "Actions happen instantly. You get a brief audio confirmation and you're back to the road.",
    icon: <CheckIcon />,
  },
];

export function HowItWorks() {
  return (
    <Section>
      <Container>
        <Reveal>
          <SectionLabel>How it works</SectionLabel>
          <DisplayHeading className="mt-5">
            Three steps.
            <br />
            That&apos;s the whole thing.
          </DisplayHeading>
        </Reveal>
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3">
          {STEPS.map((step, i) => (
            <Reveal
              key={step.num}
              delay={i * 100}
              className={[
                "border-border border-t py-10 md:border-t-0 md:py-12",
                i === 0
                  ? "md:pr-10"
                  : "md:border-l md:pr-10 md:pl-10 last:md:pr-0",
              ].join(" ")}
            >
              <span className="font-display text-accent mb-6 block text-[13px] tracking-[0.1em]">
                {step.num}
              </span>
              <div className="mb-7 size-14">{step.icon}</div>
              <h3 className="font-display text-foreground mb-3.5 text-[28px] leading-[1.15]">
                {step.title}
              </h3>
              <p className="text-muted-foreground text-[15px] leading-[1.65] font-light">
                {step.body}
              </p>
            </Reveal>
          ))}
        </div>
      </Container>
    </Section>
  );
}

function PhoneIcon() {
  return (
    <svg
      viewBox="0 0 56 56"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="size-14"
      aria-hidden
    >
      <circle
        cx="28"
        cy="28"
        r="27"
        stroke="#1A1814"
        strokeWidth="0.8"
        opacity="0.3"
      />
      <path
        d="M35.5 31.2c-1.1 0-2.2-.18-3.25-.52a.92.92 0 0 0-.95.22l-2.05 2.06a13.85 13.85 0 0 1-6.2-6.2l2.05-2.07a.94.94 0 0 0 .23-.94 10.4 10.4 0 0 1-.52-3.25c0-.51-.42-.92-.93-.92H20.5a.92.92 0 0 0-.93.92c0 8.84 7.16 16 16 16 .5 0 .93-.41.93-.92v-3.45c0-.51-.42-.93-.93-.93Z"
        stroke="#1A1814"
        strokeWidth="1.4"
        strokeLinecap="round"
        strokeLinejoin="round"
        opacity="0.9"
      />
    </svg>
  );
}

function WaveformIcon() {
  const bars = [
    { x: 14, y: 26, h: 4, o: 0.5 },
    { x: 19, y: 22, h: 12, o: 0.7 },
    { x: 24, y: 18, h: 20, o: 0.9 },
    { x: 29, y: 21, h: 14, o: 0.8 },
    { x: 34, y: 24, h: 8, o: 0.6 },
    { x: 39, y: 27, h: 3, o: 0.4 },
  ];
  return (
    <svg
      viewBox="0 0 56 56"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="size-14"
      aria-hidden
    >
      <circle
        cx="28"
        cy="28"
        r="27"
        stroke="#1A1814"
        strokeWidth="0.8"
        opacity="0.3"
      />
      {bars.map((b, i) => (
        <rect
          key={i}
          x={b.x}
          y={b.y}
          width="3"
          height={b.h}
          fill="#1A1814"
          opacity={b.o}
          rx="1"
        />
      ))}
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg
      viewBox="0 0 56 56"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="size-14"
      aria-hidden
    >
      <circle
        cx="28"
        cy="28"
        r="27"
        stroke="#1A1814"
        strokeWidth="0.8"
        opacity="0.3"
      />
      <polyline
        points="17,28 25,36 39,20"
        stroke="#1A1814"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
        opacity="0.9"
      />
    </svg>
  );
}
