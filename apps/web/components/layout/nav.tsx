import Link from "next/link";
import { Container } from "@/components/common/container";
import { CtaButton } from "@/components/common/cta-button";
import { Wordmark } from "./wordmark";

const links = [
  { label: "How it works", href: "/#how" },
  { label: "Showcase", href: "/#showcase" },
  { label: "Integrations", href: "/#integrations" },
];

export function Nav() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 backdrop-blur-md">
      <Container className="flex items-center justify-between py-5">
        <Link href="/" aria-label="OnCue home">
          <Wordmark />
        </Link>
        <nav className="hidden items-center gap-10 md:flex">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="font-heading text-muted-foreground hover:text-accent focus-visible:text-accent text-sm font-medium tracking-tight transition-colors focus-visible:outline-none"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <CtaButton disabled className="px-5 py-2.5 text-[11px]">
          Get Started
        </CtaButton>
      </Container>
    </header>
  );
}
