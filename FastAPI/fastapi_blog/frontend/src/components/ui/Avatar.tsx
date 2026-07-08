import { cn } from "@/lib/cn";

export default function Avatar({ src, size = 38, alt = "", ring }: { src?: string; size?: number; alt?: string; ring?: boolean }) {
  return (
    <span
      className={cn("inline-block rounded-full overflow-hidden shrink-0", !src && "placeholder-stripes", ring && "ring-2 ring-primary ring-offset-2 ring-offset-page")}
      style={{ width: size, height: size }}
    >
      {src && <img src={src} alt={alt} width={size} height={size} className="object-cover w-full h-full" />}
    </span>
  );
}