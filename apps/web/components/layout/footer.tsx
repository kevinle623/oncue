import Link from "next/link";
import { Wordmark } from "@/components/common/wordmark";

const LINKS = [
  { href: "/privacy", label: "Privacy", external: false },
  { href: "/terms", label: "Terms", external: false },
  {
    href: "https://github.com/kevinle623/oncue/issues",
    label: "Contact",
    external: true,
  },
];

export function Footer() {
  return (
    <footer className="border-border border-t">
      <div className="mx-auto flex max-w-[1080px] flex-col gap-6 px-6 py-12 md:flex-row md:items-center md:justify-between">
        <Wordmark size="sm" />
        <nav className="flex flex-wrap gap-7">
          {LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              {...(link.external
                ? { target: "_blank", rel: "noopener noreferrer" }
                : {})}
              className="text-muted-foreground hover:text-foreground text-xs tracking-[0.06em] uppercase transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <span className="text-muted-foreground text-xs">
          © 2026 OnCue. All rights reserved.
        </span>
      </div>
    </footer>
  );
}
