import Link from "next/link";
import { Wordmark } from "@/components/common/wordmark";

export function MobileHeader() {
  return (
    <header className="border-border bg-background/85 fixed inset-x-0 top-0 z-40 flex h-16 items-center justify-between border-b px-6 backdrop-blur-md lg:hidden">
      <Link href="/" aria-label="OnCue home">
        <Wordmark size="md" />
      </Link>
      <span className="text-muted-foreground text-[10px] tracking-[0.14em] uppercase">
        Beta
      </span>
    </header>
  );
}
