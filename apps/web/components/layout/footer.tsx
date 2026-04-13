import Link from "next/link";
import { Container } from "@/components/common/container";
import { Wordmark } from "./wordmark";

const links = [
  { label: "Privacy", href: "/privacy" },
  { label: "Terms", href: "/terms" },
  { label: "Docs", href: "/docs" },
  {
    label: "GitHub",
    href: "https://github.com/kevinle623/oncue",
    external: true,
  },
];

export function Footer() {
  return (
    <footer className="border-border bg-surface-lowest border-t">
      <Container className="flex flex-col items-center justify-between gap-8 py-12 md:flex-row">
        <div className="space-y-4 text-center md:text-left">
          <Wordmark />
          <p className="text-muted-foreground/70 max-w-xs text-sm">
            © 2026 OnCue. All rights reserved.
          </p>
        </div>
        <nav className="flex flex-wrap justify-center gap-x-8 gap-y-3">
          {links.map((link) => (
            <Link
              key={link.label}
              href={link.href}
              {...(link.external
                ? { target: "_blank", rel: "noopener noreferrer" }
                : {})}
              className="text-muted-foreground/70 hover:text-foreground text-sm transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </Container>
    </footer>
  );
}
