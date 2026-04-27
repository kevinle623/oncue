"use client";

import { useState } from "react";
import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { Reveal } from "@/components/common/reveal";
import { Section } from "@/components/common/section";
import { SectionLabel } from "@/components/common/section-label";
import { cn } from "@/lib/utils";

type Item = { q: string; a: string };

const ITEMS: Item[] = [
  {
    q: "How much does OnCue cost?",
    a: "Free during the beta. After launch, there'll be a simple monthly plan. Waitlist members get an extended free period and locked-in early pricing.",
  },
  {
    q: "Does it work on any phone?",
    a: "Yes — any phone that can make a standard call. iPhone, Android, or even a basic handset. No app required. If you can dial a number, you can use OnCue.",
  },
  {
    q: "What happens if I lose signal mid-call?",
    a: "The call ends gracefully. Any in-progress action is either completed or safely rolled back. When you reconnect, you just call again — no session to restore or resume.",
  },
  {
    q: "Can I hang up in the middle of a command?",
    a: "Anytime. Hanging up is the equivalent of pressing stop. OnCue will finish any action it's already executing, then go idle.",
  },
  {
    q: "Does it work with Bluetooth / CarPlay / Android Auto?",
    a: "Yes. Since OnCue is just a phone call, it plays through whatever audio output you already have connected — Bluetooth speakers, your car's system, a headset. It requires no special integrations with CarPlay or Android Auto.",
  },
  {
    q: "What languages are supported?",
    a: "English at launch, with Spanish, French, and German in active development. Waitlist members will get early access to new language releases.",
  },
];

export function Faq() {
  const [openIdx, setOpenIdx] = useState<number | null>(null);

  return (
    <Section>
      <Container width="narrow">
        <Reveal>
          <SectionLabel>FAQ</SectionLabel>
          <DisplayHeading className="mt-5">Questions.</DisplayHeading>
        </Reveal>
        <Reveal className="border-border mt-14 border-t">
          {ITEMS.map((item, i) => {
            const open = openIdx === i;
            return (
              <div key={item.q} className="border-border border-b">
                <button
                  type="button"
                  onClick={() => setOpenIdx(open ? null : i)}
                  aria-expanded={open}
                  className="flex w-full items-center justify-between gap-4 py-[22px] text-left"
                >
                  <span className="text-foreground text-base leading-[1.4]">
                    {item.q}
                  </span>
                  <PlusIcon open={open} />
                </button>
                <div
                  className={cn(
                    "text-muted-foreground overflow-hidden text-[15px] leading-[1.7] font-light transition-[max-height,padding] duration-[350ms] ease-in-out",
                    open ? "max-h-[300px] pb-[22px]" : "max-h-0",
                  )}
                >
                  {item.a}
                </div>
              </div>
            );
          })}
        </Reveal>
      </Container>
    </Section>
  );
}

function PlusIcon({ open }: { open: boolean }) {
  return (
    <span
      className={cn(
        "relative size-5 shrink-0 transition-opacity duration-200",
        open ? "opacity-100" : "opacity-50 group-hover:opacity-100",
      )}
    >
      <span className="bg-foreground absolute top-1/2 left-1/2 h-px w-3 -translate-x-1/2 -translate-y-1/2" />
      <span
        className={cn(
          "bg-foreground absolute top-1/2 left-1/2 h-3 w-px -translate-x-1/2 -translate-y-1/2 transition-[transform,opacity] duration-300",
          open && "rotate-90 opacity-0",
        )}
      />
    </span>
  );
}
