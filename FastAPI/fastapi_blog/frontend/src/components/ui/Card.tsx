import { cn } from "@/lib/cn";

export default function Card({ className, ...rest }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("bg-surface border border-border rounded-[16px] shadow-[var(--shadow-card)]", className)} {...rest} />;
}