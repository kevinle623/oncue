"use client";

import { useState } from "react";
import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { Reveal } from "@/components/common/reveal";
import { Section } from "@/components/common/section";

export function WaitlistCta() {
  const [email, setEmail] = useState("");
  const [invalid, setInvalid] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  function submit() {
    const trimmed = email.trim();
    if (!trimmed.includes("@")) {
      setInvalid(true);
      return;
    }
    setInvalid(false);
    setSubmitted(true);
  }

  return (
    <Section
      id="waitlist"
      tone="surface-low"
      className="text-center"
      style={{ paddingBlock: 120 }}
    >
      <Container className="max-w-[560px] px-6">
        <Reveal>
          <DisplayHeading size="lg">
            Say the word.
            <br />
            <em>We&apos;ll handle it.</em>
          </DisplayHeading>
          <p className="text-muted-foreground mt-5 mb-11 text-base leading-[1.6] font-light">
            Ready to keep your eyes on the road?
          </p>

          {submitted ? (
            <p className="text-accent text-sm tracking-[0.05em]">
              ✓ &nbsp;You&apos;re on the list. We&apos;ll be in touch.
            </p>
          ) : (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                submit();
              }}
              className="mx-auto flex max-w-[400px] flex-col gap-3 sm:flex-row"
            >
              <input
                type="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  if (invalid) setInvalid(false);
                }}
                placeholder="your@email.com"
                aria-label="Email"
                aria-invalid={invalid}
                className={[
                  "bg-surface text-foreground placeholder:text-muted-foreground flex-1 rounded-[3px] border px-[18px] py-3.5 text-sm outline-none transition-colors",
                  invalid
                    ? "border-accent"
                    : "border-border-strong focus:border-accent",
                ].join(" ")}
              />
              <button
                type="submit"
                className="bg-accent text-accent-foreground inline-flex items-center justify-center rounded-[3px] px-6 py-3.5 text-[13px] font-medium tracking-[0.07em] whitespace-nowrap uppercase transition-[opacity,transform] duration-200 hover:-translate-y-px hover:opacity-90"
              >
                Reserve spot
              </button>
            </form>
          )}
        </Reveal>
      </Container>
    </Section>
  );
}
