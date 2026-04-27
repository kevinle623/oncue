"use client";

import Link from "next/link";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";

type Size = "sm" | "md";

const sizeClass: Record<Size, string> = {
  sm: "px-5 py-[9px] text-[13px] tracking-[0.06em]",
  md: "px-10 py-4 text-sm tracking-[0.07em]",
};

const baseClass =
  "bg-accent text-accent-foreground inline-flex items-center justify-center rounded-[3px] font-medium uppercase transition-[opacity,transform,box-shadow] duration-200 hover:opacity-90 hover:-translate-y-[2px] hover:shadow-[0_8px_32px_rgba(26,24,20,0.12)]";

type CommonProps = {
  size?: Size;
  className?: string;
  children: React.ReactNode;
};

type LinkProps = CommonProps & {
  href: string;
  onClick?: never;
  type?: never;
};

type ButtonProps = CommonProps &
  Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, "className"> & {
    href?: undefined;
  };

export const PrimaryButton = forwardRef<
  HTMLButtonElement | HTMLAnchorElement,
  LinkProps | ButtonProps
>(function PrimaryButton(props, ref) {
  const { size = "md", className, children } = props;
  const merged = cn(baseClass, sizeClass[size], className);

  if ("href" in props && props.href) {
    const href = props.href;
    const isExternal = /^https?:\/\//.test(href);
    const hashMatch = href.match(/#([^?]+)$/);
    const handleClick = hashMatch
      ? (event: React.MouseEvent<HTMLAnchorElement>) => {
          if (
            event.metaKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey
          ) {
            return;
          }
          const target = document.getElementById(hashMatch[1]);
          if (!target) return;
          event.preventDefault();
          target.scrollIntoView({ behavior: "smooth", block: "start" });
          if (window.location.hash !== `#${hashMatch[1]}`) {
            history.replaceState(null, "", `#${hashMatch[1]}`);
          }
        }
      : undefined;
    return (
      <Link
        ref={ref as React.Ref<HTMLAnchorElement>}
        href={href}
        className={merged}
        onClick={handleClick}
        {...(isExternal
          ? { target: "_blank", rel: "noopener noreferrer" }
          : {})}
      >
        {children}
      </Link>
    );
  }

  const { size: _size, className: _cn, children: _ch, ...rest } = props;
  void _size;
  void _cn;
  void _ch;
  return (
    <button
      ref={ref as React.Ref<HTMLButtonElement>}
      type="button"
      {...(rest as React.ButtonHTMLAttributes<HTMLButtonElement>)}
      className={merged}
    >
      {children}
    </button>
  );
});
