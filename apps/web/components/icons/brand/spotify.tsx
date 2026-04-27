export function SpotifyGlyph(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden {...props}>
      <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm4.586 14.424a.623.623 0 01-.857.208c-2.348-1.435-5.304-1.76-8.785-.964a.623.623 0 01-.277-1.215c3.809-.87 7.076-.496 9.712 1.115a.623.623 0 01.207.856zm1.223-2.722a.78.78 0 01-1.072.257C14.22 12.27 10.855 11.91 8.12 12.7a.78.78 0 01-.437-1.495c3.115-.91 6.988-.47 9.673 1.224a.78.78 0 01.453 1.273zm.105-2.835C15.06 9.107 10.855 8.97 8.004 9.8a.937.937 0 11-.543-1.794c3.29-.998 8.16-.805 11.384 1.094a.937.937 0 11-.931 1.767z" />
    </svg>
  );
}

export function SpotifyBadge() {
  return (
    <span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-[#1DB954] text-black">
      <SpotifyGlyph className="size-[18px]" />
    </span>
  );
}
