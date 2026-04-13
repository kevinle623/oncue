import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { Container } from "@/components/common/container";
import { Eyebrow } from "@/components/common/eyebrow";
import { Footer } from "@/components/layout/footer";
import { Nav } from "@/components/layout/nav";

export function DocPage({
  eyebrow,
  title,
  updated,
  children,
}: {
  eyebrow: string;
  title: string;
  updated?: string;
  children: React.ReactNode;
}) {
  return (
    <>
      <Nav />
      <main className="flex-1 pt-32 pb-24 md:pt-40">
        <Container className="max-w-3xl">
          <Link
            href="/"
            className="text-muted-foreground hover:text-accent mb-10 inline-flex items-center gap-2 text-sm transition-colors"
          >
            <ArrowLeft className="size-4" />
            Back to home
          </Link>
          <div className="space-y-4">
            <Eyebrow tone="accent">{eyebrow}</Eyebrow>
            <h1 className="font-heading text-4xl font-black tracking-[-0.03em] md:text-6xl">
              {title}
            </h1>
            {updated && (
              <p className="text-muted-foreground text-sm">
                Last updated {updated}
              </p>
            )}
          </div>
          <div className="prose-doc mt-16 space-y-10 text-base leading-relaxed">
            {children}
          </div>
        </Container>
      </main>
      <Footer />
    </>
  );
}
