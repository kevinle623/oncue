"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { PrimaryButton } from "@/components/common/primary-button";
import { Wordmark } from "@/components/common/wordmark";
import { cn } from "@/lib/utils";

export function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 60);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <nav
      className={cn(
        "fixed inset-x-0 top-0 z-[100] flex items-center justify-between px-8 py-5 transition-[background,backdrop-filter] duration-300",
        scrolled
          ? "border-border border-b bg-[rgba(244,241,235,0.94)] backdrop-blur-[12px]"
          : "bg-gradient-to-b from-[rgba(244,241,235,0.9)] to-transparent backdrop-blur-0",
      )}
    >
      <Link href="/" aria-label="OnCue home">
        <Wordmark size="md" />
      </Link>
      <PrimaryButton href="/#waitlist" size="sm">
        Join waitlist
      </PrimaryButton>
    </nav>
  );
}
