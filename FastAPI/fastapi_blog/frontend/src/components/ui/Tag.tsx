import { cn } from "@/lib/cn";

export default function Tag({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <span className={cn("inline-flex items-center px-2.5 py-1 rounded-full bg-tint text-accent text-xs font-medium", className)}>
      {children}
    </span>
  );
}