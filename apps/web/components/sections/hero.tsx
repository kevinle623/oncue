import { PrimaryButton } from "@/components/common/primary-button";
import { HeroVisual } from "@/components/sections/hero-visual";

const fadeUp = "opacity-0 animate-[fade-up_0.8s_forwards]";

export function Hero() {
  return (
    <section className="relative flex min-h-svh flex-col items-center justify-center overflow-hidden px-6 pt-[120px] pb-20 text-center">
      <HeroVisual />

      <div className="relative z-[2] max-w-[680px]">
        <p
          className={`text-accent mb-6 text-[11px] font-medium tracking-[0.18em] uppercase ${fadeUp} [animation-delay:0.2s]`}
        >
          Hands-free AI voice assistant for drivers
        </p>
        <h1
          className={`font-display text-foreground mb-7 text-[clamp(44px,8vw,88px)] leading-[1.0] tracking-[-0.02em] ${fadeUp} [animation-delay:0.35s]`}
        >
          Drive. Speak.
          <br />
          <em>
            Everything <span className="opacity-35">on</span>Cue.
          </em>
        </h1>
        <p
          className={`text-muted-foreground mx-auto mb-11 max-w-[480px] text-[clamp(16px,2.5vw,20px)] leading-[1.5] font-light ${fadeUp} [animation-delay:0.5s]`}
        >
          Your voice is the interface.
        </p>
        <div
          className={`flex flex-col items-center gap-[14px] ${fadeUp} [animation-delay:0.65s]`}
        >
          <PrimaryButton href="#get-started">Run it yourself</PrimaryButton>
          <span className="text-muted-foreground text-xs tracking-[0.04em]">
            Open source today &nbsp;·&nbsp; Hosted product coming
          </span>
        </div>
      </div>

      <div
        className={`absolute bottom-9 left-1/2 -translate-x-1/2 ${fadeUp} [animation-delay:1.2s]`}
        aria-hidden
      >
        <div className="from-muted-foreground h-12 w-px animate-[scroll-pulse_2s_1.5s_ease-in-out_infinite] bg-gradient-to-b to-transparent" />
      </div>
    </section>
  );
}
