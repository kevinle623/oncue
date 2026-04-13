import Image, { type ImageProps } from "next/image";
import { cn } from "@/lib/utils";

type Props = Omit<ImageProps, "className"> & {
  className?: string;
  imageClassName?: string;
  fadeStart?: number;
  fadeEnd?: number;
};

export function FadedImage({
  className,
  imageClassName,
  fadeStart = 45,
  fadeEnd = 55,
  ...imageProps
}: Props) {
  const mask = `linear-gradient(to right, transparent, #000 ${fadeStart}%, #000 ${fadeEnd}%, transparent), linear-gradient(to bottom, transparent, #000 ${fadeStart}%, #000 ${fadeEnd}%, transparent)`;

  return (
    <div
      className={cn("relative", className)}
      style={{
        maskImage: mask,
        WebkitMaskImage: mask,
        maskComposite: "intersect",
        WebkitMaskComposite: "source-in",
      }}
    >
      <Image {...imageProps} className={cn("object-cover", imageClassName)} />
    </div>
  );
}
