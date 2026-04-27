import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { SectionLabel } from "@/components/common/section-label";
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
        <Container width="prose">
          <Link
            href="/"
            className="text-muted-foreground hover:text-foreground mb-10 inline-flex items-center gap-2 text-sm transition-colors"
          >
            <ArrowLeft className="size-4" />
            Back to home
          </Link>
          <div className="space-y-5">
            <SectionLabel>{eyebrow}</SectionLabel>
            <DisplayHeading as="h1" size="md">
              {title}
            </DisplayHeading>
            {updated && (
              <p className="text-muted-foreground text-sm">
                Last updated {updated}
              </p>
            )}
          </div>
          <div className="prose-doc mt-14 space-y-8 text-base leading-relaxed">
            {children}
          </div>
        </Container>
      </main>
      <Footer />
    </>
  );
}
